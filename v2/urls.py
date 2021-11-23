from django.urls import path
from v2.views import anasayfa, post_detail, category_show

urlpatterns = [
    path('', anasayfa , name='anasayfa'), #anasayfa '' bos olursa anasayfa
    path('post/<slug:slug>/', post_detail, name='detail'),  #detail post 
    path('cat/<slug:category_slug>', category_show, name='category_show'),
]