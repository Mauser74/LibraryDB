from django.contrib import messages
from django.contrib.admin.utils import QUOTE_MAP
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from lib_app.forms import BookModelForm, AuthorModelForm
from lib_app.models import Book, Cart, BorrowedBook, Author



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
        # else:
        #     queryset = Author.objects.all()
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
            f'Автор "{self.object.name}" успешно добавлен'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме'
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
            f'Данные автора "{self.object.name}" успешно обновлены'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок"""
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме'
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
        book.times_of_issued = getattr(book, 'times_of_issued', 0) + 1
        book.save(update_fields=['times_of_issued'])
        return super().get(request, *args, **kwargs)



class BookCreateView(CreateView):
    """Добавление книги"""
    model = Book
    template_name = 'lib_app/book_add.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        messages.success(self.request, 'Книга успешно добавлена')
        return super().form_valid(form)



class BookUpdateView(UpdateView):
    """Редактирование книги"""
    model = Book
    template_name = 'lib_app/book_edit.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        messages.success(self.request, 'Описание книги отредактировано')
        return super().form_valid(form)



class BookDeleteView(DeleteView):
    """Удаление книги"""
    model = Book
    template_name = 'lib_app/book_delete.html'
    success_url = reverse_lazy('book_list')



################################
# Работа с корзиной
################################

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



# @login_required
def view_cart(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'lib_app/cart.html', {'cart': cart})



@login_required
def remove_from_cart(request, book_id):
    """Убрать книгу из корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    book = get_object_or_404(Book, id=book_id)
    cart.books.remove(book)
    return redirect('view_cart')



# --- Админские действия (только для staff) ---
#@login_required
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
