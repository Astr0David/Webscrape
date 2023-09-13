# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import psycopg2


class OnepiecefandomscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name in ("appearance", "personality", "abilities_and_powers"):
                value = adapter.get(field_name)
                if value is not None:
                    cleaned_text = self.clean_text(value)
                    adapter[field_name] = cleaned_text
            elif field_name == "year":
                value = adapter.get(field_name)
                adapter[field_name] = int(value)
        return item

    def clean_text(self, text):
        clean = text.strip()

        clean = re.sub(r"\[\d+\]", "", clean)
        clean = re.sub(r"\n", "", clean)
        clean = re.sub(r"\\", "", clean)
        clean = re.sub(r" +", " ", clean)
        clean = re.sub(r"[^\x20-\x7E]+", "", clean)

        return clean


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            host="",
            database="",
            user="",
            password="",
            port =""
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS characters(
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                episode VARCHAR(15),
                chapter VARCHAR(15),
                year INTEGER,
                note TEXT,
                appearance TEXT,
                personality TEXT,
                abilities_and_powers TEXT
        )"""
        )
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            query = """
            INSERT INTO characters (name, episode, chapter, year, note, appearance, personality, abilities_and_powers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET
                episode = EXCLUDED.episode,
                chapter = EXCLUDED.chapter,
                year = EXCLUDED.year,
                note = EXCLUDED.note,
                appearance = EXCLUDED.appearance,
                personality = EXCLUDED.personality,
                abilities_and_powers = EXCLUDED.abilities_and_powers;
            """

            values = (
                item.get("name"),
                item.get("episode"),
                item.get("chapter"),
                item.get("year"),
                item.get("note"),
                item.get("appearance"),
                item.get("personality"),
                item.get("abilities_and_powers"),
            )

            self.cursor.execute(query, values)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()

            raise e

        return item
