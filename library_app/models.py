from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    """Модель автора книги"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги с привязкой к автору"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)  # доступна ли для выдачи

    def __str__(self):
        return f"{self.title} ({self.author.name})"


class Cart(models.Model):
    """Корзина пользователя: временный выбор книг перед выдачей"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return f"Корзина {self.user.username}"


class BorrowedBook(models.Model):
    """Фактически выданные книги пользователю"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        status = "возвращена" if self.returned else "выдана"
        return f"{self.user.username} — {self.book.title} ({status})"