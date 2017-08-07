# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def Home(request):
	context = {}
	return render(request, "homepage.html", context)
# Create your views here.
