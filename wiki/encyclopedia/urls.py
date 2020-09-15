from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.page, name="new_page"),
    path("edit/<str:name>",views.page,name = "edit_page"),
    path("random/",views.rand,name = "random_page"),
    path("wiki/<str:name>",views.index,name = "search")




]
