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

def search(key,names):
    temp = util.get_entry(key)   #exact word
    if temp != None:
        return temp
    else:   #matches
        arr = [i for i in names if key in i ]
        return arr


def index(request, name=False):
    print(request.GET)
    names = util.list_entries()

    if name != False:
        val = md.markdown(util.get_entry(name))
    else:
        try:
            values = search(request.GET["q"],names)
            if type(values) != "list":
                val = md.markdown(values)
                print(values)

            elif len(values) == 1:
                val = md.markdown(util.get_entry(values[0]))

            else:
                print("TRUE")
                names = values
                val = False
        except Exception as e:
            print(e)
            val = False

    return render(request, "encyclopedia/index.html", {
        "entries": names,
        "val": val
    })


# newform(   name,  class, placeholde )
def rand(request):
    names = util.list_entries()
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
