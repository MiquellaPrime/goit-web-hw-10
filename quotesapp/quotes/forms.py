from django.forms import ModelForm, CharField, TextInput

from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class AuthorForm(ModelForm):
    full_name     = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_date     = CharField(min_length=5, max_length=25, required=True, widget=TextInput())
    born_location = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description   = CharField(min_length=10, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ["full_name", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):
    quote = CharField(required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["author", "tags"]
