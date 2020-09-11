from django.shortcuts import render
from django.http import HttpResponse as hres,HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
import markdown2 as md
import random


class inputfield(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={"placeholder": "Enter Title", "id": "tbox"}))
    context = forms.CharField(label="Information", widget=forms.Textarea(
        attrs={"placeholder": "Enter Description", "id": "bbox"}))


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
def rand(request):
    names =util.list_entries()
    t = random.randint(0,len(names))
    print(names[t])
    return index(request,names[t])



def page(request):
    x = inputfield()
    same = False
    if request.method == "POST":
        try:
            if request.POST["title"].upper() not in  util.list_entries():
                util.save_entry(request.POST["title"],request.POST["context"])
                return HttpResponseRedirect(reverse("index"))
            else:
                same = True
                x = inputfield(request.POST)



        except:
            pass

    return render(request, "encyclopedia/forms.html", {
        "form":x,
        "same":same
    })
