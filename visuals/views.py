from django.shortcuts import render
from django.views.generic import CreateView, ListView, View, DetailView

from .dash_apps.finished_apps import dash1, dash2, dash3

def home(request, template_name="visuals/main.html", **kwargs):
    context = {}
    return render(request, template_name=template_name, context=context)

def demo1(request, template_name="visuals/demo1.html", **kwargs):
    context = {}
    return render(request, template_name=template_name, context=context)

def demo2(request, template_name="visuals/demo2.html", **kwargs):
    context = {}
    return render(request, template_name=template_name, context=context)

def demo3(request, template_name="visuals/demo3.html", **kwargs):
    context = {}
    return render(request, template_name=template_name, context=context)