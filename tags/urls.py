from django.urls import path
from . import views

urlpatterns = [
    path('', views.tag_list, name='tag_list'),
    path('<int:tag_id>/', views.tag_detail, name='tag_detail'),
]
