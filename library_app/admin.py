from django.contrib import admin
from models import Author, Book, Cart, BorrowedBook

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available')
    list_filter = ('available', 'author')
    search_fields = ('title', 'isbn')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ('books',)

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned')
    list_filter = ('returned', 'borrowed_at')
    actions = ['mark_as_returned', 'issue_from_cart']

    @admin.action(description="Отметить как возвращённые")
    def mark_as_returned(self, request, queryset):
        for record in queryset:
            if not record.returned:
                record.returned = True
                record.book.available = True
                record.book.save()
                record.save()
        self.message_user(request, "Выбранные книги отмечены как возвращённые.")

    @admin.action(description="Выдать книги из корзин пользователей")
    def issue_from_cart(self, request, queryset):
        # Эта операция не применяется к BorrowedBook напрямую.
        # Лучше реализовать отдельную кнопку или страницу.
        pass