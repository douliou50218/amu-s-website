from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('storage/', views.storage, name='storage'),
    path('already_sold/', views.already_sold, name='already_sold'),
    path('sold_today/', views.sold_today, name='sold_today'),
    path('add_new/', views.add_new, name='add_new'),
]