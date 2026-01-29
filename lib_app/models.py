from django.db import models

# Create your models here.

class Author(models.Model):
    """Модель автора книги"""
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(default = None)
    date_of_death = models.DateField(default = None)

    def __str__(self):
        return self.name


class Translator(models.Model):
    """Модель переводчика книги"""
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(default = None)
    date_of_death = models.DateField(default = None)

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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, related_name='books', default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    year_of_publication = models.PositiveIntegerField(default=0)
    thematic = models.TextField()                   # тематические рубрики
    key_words = models.TextField()                  # ключевые слова
    available = models.BooleanField(default=True)   # доступна ли для выдачи
    times_of_issued = models.PositiveIntegerField(default=0)    # сколько раз выдана книга


