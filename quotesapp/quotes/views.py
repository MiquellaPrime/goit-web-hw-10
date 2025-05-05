from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote


def main(request):
    quotes = Quote.objects.all().select_related("author").prefetch_related("tags")

    top_tags = Tag.objects.annotate(quotes_count=Count("quote")).order_by("-quotes_count", "name")[:10]

    return render(request, "quotes/index.html", {"quotes": quotes, "top_tags": top_tags})


@login_required
def create_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_tag.html", {"form": form})

    return render(request, "quotes/add_tag.html", {"form": TagForm()})


@login_required
def create_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AuthorForm()})


@login_required
def create_quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)

            choice_author = Author.objects.get(full_name=request.POST.get("author"))
            new_quote.author = choice_author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/add_quote.html",
                {"authors": authors, "tags": tags, "form": form}
            )

    return render(
        request,
        "quotes/add_quote.html",
        {"authors": authors, "tags": tags, "form": QuoteForm()}
    )


def get_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "quotes/author.html", {"author": author})


def get_quotes_by_tag(request, tag):
    quotes = Quote.objects.filter(tags__name=tag).select_related("author").prefetch_related("tags")
    return render(request, "quotes/tag_quotes.html", {"quotes": quotes, "tag": tag})
