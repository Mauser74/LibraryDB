from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from models import Book, Cart, BorrowedBook

@login_required
def book_list(request):
    """Список всех книг с поиском"""
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(isbn__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'query': query})


@login_required
def add_to_cart(request, book_id):
    """Добавить книгу в корзину"""
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if book.available:
        cart.books.add(book)
    return redirect('book_list')


@login_required
def view_cart(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'library/cart.html', {'cart': cart})


@login_required
def remove_from_cart(request, book_id):
    """Убрать книгу из корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    book = get_object_or_404(Book, id=book_id)
    cart.books.remove(book)
    return redirect('view_cart')


# --- Админские действия (только для staff) ---
@login_required
def issue_books_from_cart(request, user_id):
    """Админ выдаёт все книги из корзины пользователя"""
    if not request.user.is_staff:
        return redirect('book_list')

    cart = get_object_or_404(Cart, user_id=user_id)
    for book in cart.books.all():
        if book.available:
            BorrowedBook.objects.create(user=cart.user, book=book)
            book.available = False
            book.save()
    cart.books.clear()  # очищаем корзину после выдачи
    return redirect('admin:library_app_cart_changelist')