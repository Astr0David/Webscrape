import scrapy
import re
from onepiecefandomscraper.items import OnePieceCharacterItem


class CharacterspiderSpider(scrapy.Spider):
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
                            meta={"data": data},
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

        section_ids = ["Appearance", "Personality", "Abilities_and_Powers"]

        for section_id in section_ids:
            span_element = response.xpath(f'//h2/span[@id="{section_id}"]')

            if span_element:
                section_content = ""

                for sibling in span_element.xpath("ancestor::h2/following-sibling::*"):
                    if sibling.xpath("local-name()").get() == "p":
                        paragraph_text = sibling.xpath("string()").get()
                        section_content += paragraph_text + " "
                    elif sibling.xpath("local-name()").get() == "h2":
                        break

                data[section_id.lower()] = section_content

        yield data
