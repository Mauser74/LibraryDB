from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class RegisterView(FormView):
    """Форма регистрации пользователя"""
    template_name = 'user_app/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)



class CustomLoginView(LoginView):
    """Форма входа пользователя"""
    template_name = 'user_app/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('book_list')

    def get_success_url(self):
        return self.success_url



class CustomLogoutView(LogoutView):
    """Разлогинивание пользователя"""
    next_page = reverse_lazy('login')



class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Форма отображения списка пользователей библиотеки для персонала"""
    model = CustomUser
    template_name = 'user_app/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        # Исключаем персонал и суперпользователей
        return CustomUser.objects.filter(is_staff=False, is_superuser=False)



class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Форма редактирования учётной записи пользователя персоналом"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_app/user_edit.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, f'Пользователь {self.object.full_name} обновлён.')
        return super().form_valid(form)



class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Форма подтверждения удаления учётной записи пользователя персоналом"""
    model = CustomUser
    template_name = 'user_app/user_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, f'Пользователь {self.object.full_name} удалён.')
        return super().form_valid(form)