from django.shortcuts import get_object_or_404, render

from .models import Tag


def tag_list(request):
    return render(request, 'tags/tag_list.html')


def tag_detail(request):
    return render(request, 'tags/tag_detail.html')
