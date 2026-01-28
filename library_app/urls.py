from django.urls import path
import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('admin/issue-cart/<int:user_id>/', views.issue_books_from_cart, name='issue_books_from_cart'),
]