from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.showEntry, name="showEntry"),
    path("errorNoEntry", views.errorNoEntry, name="errorNoEntry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("edit", views.edit, name="edit"),
    path("editedPage", views.editedPage, name="editedPage")


]
