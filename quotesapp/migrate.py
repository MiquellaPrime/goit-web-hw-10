import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotesapp.settings")

import django
django.setup()

from mongoengine import connect, Document, StringField, ListField, ReferenceField
from pydantic_settings import BaseSettings, SettingsConfigDict

from quotes.models import Author, Quote, Tag


class BaseSettingsWithConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")


class MongoDBSettings(BaseSettingsWithConfig):
    model_config = SettingsConfigDict(env_prefix="mongo_")

    user:   str
    passwd: str
    domain: str
    name:   str

    @property
    def uri(self) -> str:
        return f"mongodb+srv://{self.user}:{self.passwd}@{self.domain}/?retryWrites=true&w=majority&appName={self.name}"


class Settings(BaseSettingsWithConfig):
    mongo: MongoDBSettings = MongoDBSettings()


local_settings = Settings()


connect(host=local_settings.mongo.uri, ssl=True)


class AuthorODM(Document):
    fullname      = StringField(required=True)
    born_date     = StringField()
    born_location = StringField()
    description   = StringField()


class QuoteODM(Document):
    tags   = ListField(StringField())
    author = ReferenceField(AuthorODM, required=True)
    quote  = StringField(required=True)


def migrate():
    print("Start migrating data from MongoDB to Postgres...")

    print("Authors...")
    for author_odm in AuthorODM.objects:
        Author.objects.get_or_create(
            full_name=author_odm.fullname,
            born_date=author_odm.born_date,
            born_location=author_odm.born_location,
            description=author_odm.description
        )

    print("Quotes and Tags...")
    for quote_odm in QuoteODM.objects:
        author = Author.objects.get(full_name=quote_odm.author.fullname)

        quote = Quote.objects.create(
            quote=quote_odm.quote,
            author=author
        )

        for tag_name in quote_odm.tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

    print("Done!")


if __name__ == "__main__":
    migrate()
