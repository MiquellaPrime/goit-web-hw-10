from django import template
from django.urls import reverse
from django.utils.html import mark_safe

register = template.Library()


@register.filter(name="tags", is_safe=True)
def tags(quote_tags):
    links = []
    for tag in quote_tags.all().order_by("name"):
        url = reverse("quotes:quotes_by_tag", args=[tag.name])
        links.append(f'<a href="{url}" class="secondary">#{tag.name}</a>')
    return mark_safe(" ".join(links))
