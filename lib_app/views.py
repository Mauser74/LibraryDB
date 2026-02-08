from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from lib_app.models import Book, Cart, BorrowedBook


# Create your views here.

def index(request):
    """Главная страница"""
    return render(request, 'lib_app/index.html')


def about(request):
    """Страница о нас"""
    return HttpResponse('<h1>О нас!</h1>')


#@login_required
def add_to_cart(request, book_id):
    """Добавить книгу в корзину"""
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if book.available:
        cart.books.add(book)
        messages.success(request, f'Книга "{book.title}" добавлена в корзину.')
    else:
        messages.error(request, f'Книга "{book.title}" сейчас недоступна.')
    return redirect('book_list')


#@login_required # Требование авторизации пользователя для доступа к этой странице
def book_list(request):
    """Список всех книг с поиском"""
    # Извлекает значение параметра q из URL, если q не задан — возвращает пустую строку ''
    query = request.GET.get('q', '')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(isbn__icontains=query)
        )
    else:
        books = Book.objects.all()

    context = {
        'title': 'Выбор книг',
        'books': books,
        'query': query,
    }

    return render(request, 'lib_app/book_list.html', context)


def book_detail(request, book_id):
    """Детальная информация о книге"""
    book = get_object_or_404(Book, pk=book_id)

    context = {
        'title': f'Подробнее о {book.title}',
        'book': book,
    }

    return render(request, 'lib_app/book_detail.html', context)


# @login_required
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
