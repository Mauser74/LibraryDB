from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta

# Create your models here.

class Author(models.Model):
    """Модель автора книги"""
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def clean(self):
        """
        Проверяет логическую корректность дат жизни.
        Вызывается при валидации формы или при вызове full_clean().
        """
        if self.date_of_birth and self.date_of_death:
            if self.date_of_birth > self.date_of_death:
                raise ValidationError(
                    "Дата рождения не может быть позже даты смерти."
                )
        if self.date_of_death and self.date_of_death > date.today():
            raise ValidationError(
                "Дата смерти не может быть в будущем."
            )

    def save(self, *args, **kwargs):
        """
        Переопределяем save(), чтобы автоматически вызывать валидацию.
        """
        self.full_clean()  # вызывает clean() и другие валидации
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Translator(models.Model):
    """Модель переводчика книги"""
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def clean(self):
        """
        Проверяет логическую корректность дат жизни.
        Вызывается при валидации формы или при вызове full_clean().
        """
        if self.date_of_birth and self.date_of_death:
            if self.date_of_birth > self.date_of_death:
                raise ValidationError(
                    "Дата рождения не может быть позже даты смерти."
                )
        if self.date_of_death and self.date_of_death > date.today():
            raise ValidationError(
                "Дата смерти не может быть в будущем."
            )

    def save(self, *args, **kwargs):
        """
        Переопределяем save(), чтобы автоматически вызывать валидацию.
        """
        self.full_clean()  # вызывает clean() и другие валидации
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(models.Model):
    """Модель пользователя библиотеки"""
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)

    def clean(self):
        """
        Проверяет возраст.
        Вызывается при валидации формы или при вызове full_clean().
        """
        if self.date_of_birth:
            if self.date_of_birth > date.today() + timedelta(days=7 * 365):
                raise ValidationError(
                    "Возраст не может быть меньше 7 лет."
                )

    def save(self, *args, **kwargs):
        """
        Переопределяем save(), чтобы автоматически вызывать валидацию.
        """
        self.full_clean()  # вызывает clean() и другие валидации
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Модель издательства книги"""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги с привязкой к автору"""
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        blank=True
    )
    translator = models.ForeignKey(
        Translator,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        blank=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        blank=True
    )
    isbn = models.CharField(
        max_length=13,                                          # ISBN должен содержать ровно 13 цифр
        unique=True,
        null=True,
        blank=True
    )
    # Год издания
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),                               # Год должен быть ≥ 1
            MaxValueValidator(datetime.now().year)              # Не больше текущего года
        ]
    )
    thematic = models.TextField(default = "")                   # тематические рубрики
    key_words = models.TextField(default = "")                  # ключевые слова
    available = models.BooleanField(default=True)               # доступна ли для выдачи
    times_of_issued = models.PositiveIntegerField(default=0)    # сколько раз выдана книга

    def __str__(self):
        return f"{self.author}, {self.title}"


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