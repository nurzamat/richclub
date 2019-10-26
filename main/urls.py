from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage, name='MainPage'),
    path('news', NewsList, name='NewsList'),
    path('news/<int:id>', NewsDetail, name='NewsDetail'),
    path('slides/<int:id>', SlideDetail, name='SlideDetail'),
]
