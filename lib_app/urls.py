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
from .views import remove_from_cart, issue_books_from_cart, view_cart, add_to_cart
from .views import (
    AuthorListView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    IndexTemplateView,
    AboutTemplateView,
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
    path('about/', AboutTemplateView.as_view(), name='about'),
    #path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('admin/issue-cart/<int:user_id>/', issue_books_from_cart, name='issue_books_from_cart'),
]
