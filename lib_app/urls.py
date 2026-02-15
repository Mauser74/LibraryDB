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
from .views import index, about, book_list, view_cart, add_to_cart, remove_from_cart, issue_books_from_cart, \
    book_detail, book_add, book_edit

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/add/', book_add, name='book_add'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('book/<int:book_id>/edit/', book_edit, name='book_edit'),
    path('about/', about, name='about'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('admin/issue-cart/<int:user_id>/', issue_books_from_cart, name='issue_books_from_cart'),
]
