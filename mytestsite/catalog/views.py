from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site"""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The all() is implied by default
    num_authors = Author.objects.count()


    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
    }

    #Render the html template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

#Generic book list view
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.filter(title__icontains="computer")[:5]  #Get 5 books containing the title "dream"
    template_name = 'catalog/book_list.html'  #Specify your own template name/location


class BookDetailView(generic.DetailView):
    model = Book



from django.shortcuts import get_object_or_404


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request,'catalog/book_detail.html', context={'book': book})


