from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Book,Download
from .utils import get_client_ip

class  BookListView(ListView):
    model = Book
    #queryset = Book.objects.published()
    template_name = "books/home.html"
    paginate_by = 10
    context_object_name = 'books'

    def get_queryset(self):
        try:
            query = self.request.GET.get('q')
            print(query)
            print("aaaa")
        except:
            query = None
            print("bbbb")

        if query == '' or query == None:
            object_list = Book.objects.all()
        else :
            print("cccc " +query)
            object_list = Book.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
                | Q(author__full_name__icontains=query)
            )


        return object_list


class  BookDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"


def download_book(request,slug):
    obj = {}
    book = get_object_or_404(Book, slug=slug)
    client_ip = get_client_ip(request)
    if True:
        obj['success'] = True
        obj['url'] = book.file.url

        download = Download()
        download.book = book
        download.ip_address = client_ip
        download.save()
    else:
        obj['success'] = False

    return JsonResponse(obj)
