from django.contrib import admin
from .models import Book, Author, Translator, Publisher, Cart, User, BorrowedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'publisher', 'available', 'times_of_issued')
    ordering = ('author', 'title',)
    search_fields = ('title', 'author',)
    search_help_text = 'Введите часть заголовка или имени автора для поиска в каталоге'
    readonly_fields = ('times_of_issued',)



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    ordering = ('name',)



@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    ordering = ('name',)



@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    ordering = ('name',)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    ordering = ('name', 'date_of_birth',)



@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    pass



# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'books')
