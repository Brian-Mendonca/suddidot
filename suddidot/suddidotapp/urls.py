from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>', views.category, name='category'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('search/', views.search, name='search'),
]