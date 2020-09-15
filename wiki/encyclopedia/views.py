from django.shortcuts import render,redirect
from django.http import HttpResponse as hres,HttpResponseRedirect
from . import util
from django import forms
from django.template import loader
from django.urls import reverse
import markdown2 as md
import random


class inputfield(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={"placeholder": "Enter Title", "id": "tbox"}))
    context = forms.CharField(label="Information", widget=forms.Textarea(
        attrs={"placeholder": "Enter Description", "id": "bbox"}))

def search(name):

    temp = util.get_entry(name)   #exact word
    if temp != None:
        return temp,1
    else:   #matches
        arr = []
        for i in util.list_entries():

            if name in i:
                arr += [i]
        return arr,0


def index(request, name=False):
    body, names = False,False
    compare = lambda x: md.markdown(x[0]) if x[1] ==1 else False
    if name != False:

        names,found = search(name)
        body = compare([names,found])


    else:

        try:
            names, found = search(request.GET["q"])
            body = compare([names,found])
        except:
            names = util.list_entries()

    if len(names) == 0:
        template = loader.get_template("encyclopedia/error.html")
        return hres(template.render())
    return render(request, "encyclopedia/index.html", {
        "entries": names,
        "val": body ,
        "title":name
    })


# newform(   name,  class, placeholde )
def rand(request):
    names = util.list_entries()
    t = random.randint(0,len(names)-1)
    print(names[t])
    #return index(request,names[t])
    return redirect("search",name = names[t])




def page(request,name = False):
    x = inputfield()
    print(type(request.GET))
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
    else:
        x = inputfield(initial={"title":name,"context":util.get_entry(name)})
    return render(request, "encyclopedia/forms.html", {
        "form":x,
        "same":same
    })
