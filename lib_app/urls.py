"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import (
    AuthorListView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView,
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView,
    PublisherListView, PublisherCreateView, PublisherUpdateView, PublisherDeleteView,
    CartView, AddToCartView, RemoveFromCartView, IssueBooksFromCartView,
    IndexTemplateView, AboutTemplateView,
)

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('author/add/', AuthorCreateView.as_view(), name='author_add'),
    path('author/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author_delete'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/add/', BookCreateView.as_view(), name='book_add'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('publishers/', PublisherListView.as_view(), name='publisher_list'),
    path('publisher/add/', PublisherCreateView.as_view(), name='publisher_add'),
    path('publisher/<int:pk>/edit/', PublisherUpdateView.as_view(), name='publisher_edit'),
    path('publisher/<int:pk>/delete/', PublisherDeleteView.as_view(), name='publisher_delete'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('cart/add/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:book_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('staff/issue-cart/<int:user_id>/', IssueBooksFromCartView.as_view(), name='issue_books_from_cart'),
    path('staff/users-with-cart/', views.UsersWithCartView.as_view(), name='users_with_cart'),
    path('my-borrowed/', views.MyBorrowedBooksView.as_view(), name='my_borrowed_books'),
    path('staff/borrowing-users/', views.BorrowingUsersListView.as_view(), name='borrowing_users_list'),
    path('staff/user/<int:user_id>/borrowed/', views.UserBorrowedBooksDetailView.as_view(), name='user_borrowed_books_detail'),
    path('staff/return-book/<int:book_id>/', views.ReturnBookView.as_view(), name='return_book'),
    path('about/', AboutTemplateView.as_view(), name='about'),
]
