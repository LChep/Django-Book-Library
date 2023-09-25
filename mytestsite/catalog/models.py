from django.db import models

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text = 'Enter a book genre (e.g. Science fiction)')


    def __str__(self):
        return self.name


from django.urls import reverse

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)"""
    title = models.CharField (max_length=200)

    #Foreign key used because book can only have one author but author can have multiple books
    #Author is a string rather than an object because it has not been declared anywhere in the file
    author = models.ForeignKey ("Author", on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    #ManyToMany field used because genre can contain many books. Books can cover many genres.
    #Genre class has already been defined so we can specify the object above
    genre = models.ManyToManyField (Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Return a URL to access a detail record for this book"""
        return reverse('book_detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

        display_genre.short_description = 'Genre'    


import uuid #Required for unique book instances

class BookInstance(models.Model):
    """Model representing a unique copy of a book that can be borrrowed from the library"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book across the whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
     )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
     )


    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the model object"""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
       ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Return a URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    