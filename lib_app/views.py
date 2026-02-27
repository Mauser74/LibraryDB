from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from lib_app.forms import BookModelForm, AuthorModelForm, PublisherModelForm
from lib_app.models import Book, Cart, BorrowedBook, Author, Publisher
from user_app.models import CustomUser


class IndexTemplateView(TemplateView):
    template_name = 'lib_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context



class AboutTemplateView(TemplateView):
    template_name = 'lib_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О библиотеке'
        return context



################################
# Работа с Авторами
################################

class AuthorListView(ListView):
    """Список всех авторов"""
    model = Author
    template_name = 'lib_app/author_list.html'
    context_object_name = 'authors'     # вместо object_list
    paginate_by = 20                    # выводим по 20 позиций

    def get_queryset(self):
        queryset = super().get_queryset()
        # Извлекает значение параметра q из URL, если q не задан — возвращает пустую строку ''
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['page_title'] = 'Список авторов'
        context['search_query'] = query  # чтобы отобразить запрос в форме
        return context



class AuthorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Добавление автора"""
    model = Author
    form_class = AuthorModelForm
    template_name = 'lib_app/author_add.html'
    success_url = reverse_lazy('author_list')
    permission_required = 'lib_app.add_author'
    context_object_name = 'author'

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Автор "{self.object.name}" успешно добавлен.'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)



class AuthorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование автора"""
    model = Author
    form_class = AuthorModelForm
    template_name = 'lib_app/author_edit.html'
    success_url = reverse_lazy('author_list')
    permission_required = 'lib_app.change_author'

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Данные автора "{self.object.name}" успешно обновлены.'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)



class AuthorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление автора"""
    model = Author
    template_name = 'lib_app/author_delete.html'
    success_url = reverse_lazy('author_list')
    permission_required = 'lib_app.delete_author'

    def form_valid(self, form):
        if self.object.books.exists():
            messages.error(
                self.request,
                f'Невозможно удалить автора "{self.object.name}": у него есть книги в системе.'
            )
            return HttpResponseRedirect(self.get_success_url())

        messages.success(
            self.request,
            f'Автор "{self.object.name}" успешно удалён.'
        )
        return super().form_valid(form)



################################
# Работа с Книгами
################################

class BookListView(ListView):
    """Список всех книг"""
    model = Book
    template_name = 'lib_app/book_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Извлекает значение параметра q из URL, если q не задан — возвращает пустую строку ''
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(isbn__icontains=query) |
                Q(key_words__icontains=query)
            )
        else:
            queryset = Book.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Список книг'
        return context



class BookDetailView(DetailView):
    """Детальная информация о книге"""
    model = Book

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        Book.objects.filter(pk=book.pk).update(times_of_issued=F('times_of_issued') + 1)
        return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     book = self.get_object()
    #     book.times_of_issued = getattr(book, 'times_of_issued', 0) + 1
    #     book.save(update_fields=['times_of_issued'])
    #     return super().get(request, *args, **kwargs)



class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Добавление книги"""
    model = Book
    template_name = 'lib_app/book_add.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book_list')
    permission_required = 'lib_app.add_book'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Книга "{self.object.title}" успешно добавлена.'
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)



class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование книги"""
    model = Book
    template_name = 'lib_app/book_edit.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book_list')
    permission_required = 'lib_app.change_book'

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Сведения о книге "{self.object.title}" успешно обновлены.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        book = self.get_object()
        if not book.available and not request.user.is_superuser:
            messages.error(request, 'Недоступные книги нельзя редактировать.')
            return redirect('book_list')
        return super().dispatch(request, *args, **kwargs)



class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление книги"""
    model = Book
    template_name = 'lib_app/book_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'lib_app.delete_book'

    def form_valid(self, form):
        book = self.get_object()

        # Проверка: есть ли выданные экземпляры
        if BorrowedBook.objects.filter(book=book, returned=False).exists():
            messages.error(
                self.request,
                f'Невозможно удалить книгу «{book.title}»: она сейчас выдана пользователю.'
            )
            return HttpResponseRedirect(self.success_url)

        # Проверка: есть ли в корзинах
        if Cart.objects.filter(books=book).exists():
            messages.error(
                self.request,
                f'Невозможно удалить книгу «{book.title}»: она находится в корзине одного из пользователей.'
            )
            return HttpResponseRedirect(self.success_url)

        # Если всё чисто — удаляем
        messages.success(
            self.request,
            f'Книга «{book.title}» успешно удалена.'
        )
        return super().form_valid(form)



################################
# Работа с издательствами
################################

class PublisherListView(ListView):
    """Список всех издательств"""
    model = Publisher
    template_name = 'lib_app/publisher_list.html'
    context_object_name = 'publishers'   # вместо object_list
    paginate_by = 20                     # выводим по 20 позиций

    def get_queryset(self):
        queryset = super().get_queryset()
        # Извлекает значение параметра q из URL, если q не задан — возвращает пустую строку ''
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['page_title'] = 'Список издательств'
        context['search_query'] = query  # чтобы отобразить запрос в форме
        return context



class PublisherCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Добавление издательства"""
    model = Publisher
    form_class = PublisherModelForm
    template_name = 'lib_app/publisher_add.html'
    success_url = reverse_lazy('publisher_list')
    permission_required = 'lib_app.add_publisher'

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Издательство "{self.object.name}" успешно добавлено.'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)



class PublisherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование издательства"""
    model = Publisher
    form_class = PublisherModelForm
    template_name = 'lib_app/publisher_edit.html'
    success_url = reverse_lazy('publisher_list')
    permission_required = 'lib_app.change_publisher'

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Данные издательства "{self.object.name}" успешно обновлены.'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)



class PublisherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление издательства"""
    model = Publisher
    template_name = 'lib_app/publisher_delete.html'
    success_url = reverse_lazy('publisher_list')
    permission_required = 'lib_app.delete_publisher'

    def form_valid(self, form):
        if self.object.books.exists():
            messages.error(
                self.request,
                f'Невозможно удалить издательство "{self.object.name}": у него есть книги в системе.'
            )
            return HttpResponseRedirect(self.get_success_url())

        messages.success(
            self.request,
            f'Издательство "{self.object.name}" успешно удалено.'
        )
        return super().form_valid(form)



################################
# Работа с корзиной
################################

class CartView(LoginRequiredMixin, DetailView):
    """Просмотр корзины пользователя (для обычных пользователей)"""
    model = Cart
    template_name = 'lib_app/cart.html'
    context_object_name = 'cart'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            messages.warning(request, 'У персонала нет личной корзины.')
            return redirect('book_list')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Получаем или создаём корзину текущего пользователя
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_cart'] = True
        return context



class AddToCartView(LoginRequiredMixin, View):
    """Добавить книгу в корзину"""
    def post(self, request, book_id):
        if request.user.is_staff:
            messages.error(request, 'Персонал не может добавлять книги в корзину.')
            return redirect('book_list')

        book = get_object_or_404(Book, id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        if book.available:
            cart.books.add(book)
            messages.success(request, f'Книга "{book.title}" добавлена в корзину.')
        else:
            messages.error(request, f'Книга "{book.title}" сейчас недоступна.')

        return redirect('book_list')



class RemoveFromCartView(LoginRequiredMixin, View):
    """Убрать книгу из корзины"""
    def post(self, request, book_id):
        cart = get_object_or_404(Cart, user=request.user)
        book = get_object_or_404(Book, id=book_id)
        cart.books.remove(book)
        return redirect('view_cart')



class StaffRemoveFromCartView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Админ убирает книгу из корзины пользователя"""
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, user_id, book_id):
        cart = get_object_or_404(Cart, user_id=user_id)
        book = get_object_or_404(Book, id=book_id)
        cart.books.remove(book)
        messages.success(request, f'Книга "{book.title}" удалена из корзины пользователя {cart.user.full_name}.')
        return redirect('staff_view_user_cart', user_id=user_id)



class IssueBooksFromCartView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Админ выдаёт все книги из корзины пользователя"""
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, user_id):
        cart = get_object_or_404(Cart, user_id=user_id)
        for book in cart.books.all():
            if book.available:
                BorrowedBook.objects.create(user=cart.user, book=book)
                book.available = False
                book.save()
        cart.books.clear()
        messages.success(request, f'Книги из корзины пользователя {cart.user.full_name} выданы.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



class UsersWithCartView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Список пользователей с непустыми корзинами"""
    model = Cart
    template_name = 'lib_app/users_with_cart.html'
    context_object_name = 'carts'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Cart.objects.filter(books__isnull=False).distinct()



class MyBorrowedBooksView(LoginRequiredMixin, ListView):
    """Просмотр пользователем взятых книг"""
    model = BorrowedBook
    template_name = 'lib_app/my_borrowed_books.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return BorrowedBook.objects.filter(user=self.request.user).order_by('-borrowed_at')



class BorrowingUsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Просмотр персоналом списка пользователей с выданными книгами"""
    model = CustomUser
    template_name = 'lib_app/borrowing_users_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        # Только пользователи, у которых есть хотя бы одна выданная книга
        return CustomUser.objects.filter(borrowedbook__isnull=False).distinct()



class UserBorrowedBooksDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Просмотр персоналом выданных книг конкретного пользователя"""
    model = CustomUser
    template_name = 'lib_app/user_borrowed_books_detail.html'
    context_object_name = 'borrower'
    pk_url_kwarg = 'user_id'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrowed_books'] = BorrowedBook.objects.filter(user=self.object).order_by('-borrowed_at')
        return context



class ReturnBookView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Персонал возвращает книгу"""
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, book_id):
        borrowed = get_object_or_404(BorrowedBook, id=book_id, returned=False)
        borrowed.returned = True
        borrowed.returned_at = timezone.now()
        borrowed.save()

        # Делаем книгу доступной
        book = borrowed.book
        book.available = True
        book.save()

        messages.success(request, f'Книга "{book.title}" успешно возвращена.')
        return redirect('user_borrowed_books_detail', user_id=borrowed.user.id)



class StaffViewUserCartView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Персонал смотрит корзину конкретного пользователя"""
    model = Cart
    template_name = 'lib_app/cart.html'
    context_object_name = 'cart'

    def test_func(self):
        return self.request.user.is_staff

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_cart'] = False
        return context
