from turtle import title
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from django import forms
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def showEntry(request, entry):
    entry_info = mdTohtml(entry)
    if entry_info is None:
        return render(request, "encyclopedia/errorNoEntry.html", {
            "message": "This entry does not exist"
        })
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "info": entry_info
    })


def errorNoEntry(request):
    return render(request, "encyclopedia/errorNoEntry.html")


def mdTohtml(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def search(request):
    if request.method == "POST":
        WordSearch = request.POST['q']
        html_info = mdTohtml(WordSearch)
        if html_info is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": WordSearch,
                "info": html_info
            })
        else:
            words = util.list_entries()
            suggested = []
            for entry in words:
                if WordSearch.lower() in entry.lower():
                    # was trying to find a way to get it also to route to the error page if some of the letters were not in any of the entries
                    # if WordSearch.lower() not in entry.lower():
                    # return render(request, "encyclopedia/errorNoEntry.html", {
                    #     "message": "No entries have these key letters"
                    # })
                    suggested.append(entry)
            return render(request, "encyclopedia/search.html", {
                "suggested": suggested
            })


def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newPage.html")
    else:
        title = request.POST['title']
        info = request.POST['info']
        alreadyTitle = util.get_entry(title)
        if alreadyTitle is not None:
            return render(request, "encyclopedia/errorNoEntry.html", {
                "message": "Title is already in use, try another one..."})
        else:
            util.save_entry(title, info)
            htmlInfo = mdTohtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "info": htmlInfo
            })


def randomPage(request):
    words = util.list_entries()
    word = random.choice(words)
    html_info = mdTohtml(word)
    return render(request, "encyclopedia/entry.html", {
        "title": word,
        "info": html_info
    })


def edit(request):
    if request.method == "POST":
        title = request.POST['entry']
        info = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "info": info
        })


def editedPage(request):
    if request.method == "POST":
        title = request.POST["title"]
        info = request.POST['info']
        util.save_entry(title, info)
        htmlInfo = mdTohtml(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "info": htmlInfo
        })
