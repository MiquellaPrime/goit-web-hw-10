from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("add/quote", views.create_quote, name="add_quote"),
    path("add/author", views.create_author, name="add_author"),
    path("add/tag", views.create_tag, name="add_tag"),
    path("author/<int:author_id>", views.get_author, name="author"),
    path("tag/<str:tag>", views.get_quotes_by_tag, name="quotes_by_tag"),
]
