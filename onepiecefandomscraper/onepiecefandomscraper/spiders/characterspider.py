import scrapy
import re
from onepiecefandomscraper.items import OnePieceCharacterItem


class CharacterspiderSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping character data from the One Piece Fandom website.

    This spider crawls the "List of Canon Characters" page on the One Piece Fandom
    website to collect information about various One Piece characters, including their
    names, appearances, personalities, abilities, and more. It also follows links to
    individual character pages to gather additional details.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The allowed domains for crawling.
        start_urls (list): The initial URLs to start crawling.

    Methods:
        parse: Parses the main character list page and initiates requests for individual character pages.
        parse_detailed_page: Parses individual character pages for additional information.
    """

    name = "characterspider"
    allowed_domains = ["onepiece.fandom.com"]
    start_urls = ["https://onepiece.fandom.com/wiki/List_of_Canon_Characters"]

    def parse(self, response):
        table = response.css("table.wikitable")[0]

        tbody = table.css("tbody")[0]

        tr_elements = tbody.css("tr")

        for tr in tr_elements:
            td_elements = tr.css("td")

            data = OnePieceCharacterItem()

            for idx, td in enumerate(td_elements):
                if idx == 1:
                    data["name"] = td.css("a::text").get()

                    link = td.css("a::attr(href)").get()
                    if link:
                        yield scrapy.Request(
                            url=f"https://onepiece.fandom.com{link}",
                            callback=self.parse_detailed_page,
                            meta={"data": data, "link": link},
                        )

                elif idx in (2, 3):
                    title_text = td.xpath("string()").get()
                    if title_text:
                        if idx == 2:
                            data[
                                "episode"
                            ] = f"Episode {title_text.strip().lstrip('0')}"
                        elif idx == 3:
                            data[
                                "chapter"
                            ] = f"Chapter {title_text.strip().lstrip('0')}"

                elif idx in (4, 5):
                    raw_text = td.xpath("string()").get()
                    if raw_text:
                        if idx == 4:
                            data["year"] = raw_text.strip()
                        elif idx == 5:
                            data["note"] = raw_text.strip() if raw_text else None

    def parse_detailed_page(self, response):
        data = response.meta.get("data")
        link = response.meta.get("link")

        section_ids = ["Appearance", "Personality", "Abilities_and_Powers"]
        filled_sections = set()

        for section_id in section_ids:
            span_element = response.xpath(f'//h2/span[@id="{section_id}"]')

            if span_element:
                section_content = ""

                for sibling in span_element.xpath("ancestor::h2/following-sibling::*"):
                    if sibling.xpath("local-name()").get() == "p":
                        paragraph_text = sibling.xpath("string()").get()
                        section_content += paragraph_text + " "
                    elif sibling.xpath("local-name()").get() in ("h2", "h3"):
                        if section_content != "":
                            break
                        span_element = response.xpath(f'//h3/span[@id="{section_id}"]')
                        if span_element:
                            for sibling in span_element.xpath(
                                "ancestor::h3/following-sibling::*"
                            ):
                                if sibling.xpath("local-name()").get() == "p":
                                    paragraph_text = sibling.xpath("string()").get()
                                    section_content += paragraph_text + " "
                                elif sibling.xpath("local-name()").get() in ("h2"):
                                    break

                data[section_id.lower()] = section_content
                filled_sections.add(section_id.lower())

        if len(filled_sections) == len(section_ids):
            yield data
        else:
            for section_id in section_ids:
                if section_id not in filled_sections:
                    if section_id == "Personality":
                        yield scrapy.Request(
                            url=f"https://onepiece.fandom.com/{link}/Personality_and_Relationships",
                            callback=self.check_external_link,
                            meta={
                                "data": data,
                                "section-id": "Personality",
                                "filled-sections": filled_sections,
                            },
                        )
                    elif section_id == "Abilities_and_Powers":
                        yield scrapy.Request(
                            url=f"https://onepiece.fandom.com/{link}/Abilities_and_Powers",
                            callback=self.check_external_link,
                            meta={
                                "data": data,
                                "section-id": "Abilities_and_Powers",
                                "filled-sections": filled_sections,
                            },
                        )

    def check_external_link(self, response):
        data = response.meta.get("data")
        section_id = response.meta.get("section-id")
        filled_sections = response.meta.get("filled-sections")

        span_element = (
            response.xpath(f'//h2/span[@id="{section_id}"]')
            or response.xpath('//h2/span[@id="Overview"]')
        )

        if span_element:
            section_content = ""

            for sibling in span_element.xpath("ancestor::h2/following-sibling::*"):
                if sibling.xpath("local-name()").get() == "p":
                    paragraph_text = sibling.xpath("string()").get()
                    section_content += paragraph_text + " "
                elif sibling.xpath("local-name()").get() == "h3":
                    if sibling.xpath("span[@id!='Overview']").get() is not None:
                        break
                elif sibling.xpath("local-name()").get() in ("h2", "h3"):
                    break

        data[section_id.lower()] = section_content
        filled_sections.add(section_id.lower())

        if len(filled_sections) == 3:
            yield data
