from django.shortcuts import render
from django.http import HttpResponse as hres
from . import util
from django import forms
import markdown2 as md


class head(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={"placeholder": "Enter Title", "id": "tbox"})
                            )


class body(forms.Form):
    context = forms.CharField(label="Information", widget=forms.Textarea(
        attrs={"placeholder": "Enter Description", "id": "bbox"})
                              )


def index(request, name=False):
    if name != False:
        q = util.get_entry(name)
        val = md.markdown(q)
    else:
        val = False
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "val": val
    })


# newform(   name,  class, placeholde )


def page(request):   #server side validation, title validation  
    if request.method == "POST":
        util.save_entry(request.POST["title"],request.POST["context"])


    return render(request, "encyclopedia/forms.html", {
        "title": head(),
        "body": body()
    })
