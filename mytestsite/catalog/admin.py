from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

#admin.site.register (Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]


#admin.site.register (Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    
#Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


admin.site.register (Genre)

#admin.site.register (BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

