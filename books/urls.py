from django.contrib import admin
from django.urls import path
from books.views import BookListView,BookDetailView,download_book

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('<str:slug>', BookDetailView.as_view(), name='detail'),
    path('download-book/<str:slug>', download_book, name='download-book'),
]
