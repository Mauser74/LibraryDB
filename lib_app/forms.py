from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Book


class BookForm(forms.Form):
    """Форма добавления книги"""
    title = forms.CharField(
        max_length=255,
        label='Название книги',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите название'}
        ),
    )
    author = forms.CharField(
        label='Автор',
    )
    translator = forms.CharField(
        label='Переводчик',
    )
    publisher = forms.CharField(
        label='Издатель',
    )
    isbn = forms.CharField(
        label='ISBN',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ISBN'}
        ),
    )
    year = forms.IntegerField(
        label='Год издания',
        min_value = 1,
        max_value = datetime.now().year,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите год'}
        ),
    )
    short_description = forms.CharField(
        label='Краткое описание',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите описание'}
        ),
    )
    keywords = forms.CharField(
        label='Ключевые слова',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ключевые слова'}
        ),
    )
    available = forms.BooleanField(
        label='Доступность для получения',
        widget=forms.CheckboxInput()
    )
    times_of_issued = forms.IntegerField(
        label='Сколько раз книга выдана',
    )


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        # Определяет порядок следования полей на странице
        fields = (
            'title',
            'author',
            'translator',
            'publisher',
            'isbn',
            'year',
            'short_description',
            'key_words',
            'times_of_issued',
            'available',
        )
        # Названия полей
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'translator': 'Переводчик',
            'publisher': 'Издательство',
            'isbn': 'ISBN',
            'year': 'Год издания',
            'short_description': 'Краткое описание',
            'key_words': 'Ключевые слова',
            'available': 'Доступна для выдачи',
            'times_of_issued': 'Выдана раз',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'translator': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 32, 'placeholder': 'Введите ISBN'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год издания'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание книги'}),
            'key_words': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ключевые слова'}),
            'times_of_issued': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сколько раз книга выдана'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'width: 20px; height: 20px;'}),
        }

    def clean_title(self):
        """Валидация названия книги"""
        title = self.cleaned_data.get('title')
        if len(title) > 255:
            raise ValidationError('Слишком длинное название (более 255 символов)')
        elif len(title) == 1:
            raise ValidationError('Название не должно быть пустым')
        return title

    # def clean_isbn(self):
    #     isbn = self.cleaned_data.get('isbn')
    #     clean_isbn = ''.join(char for char in isbn if char.isdigit())
    #     if len(clean_isbn) > 13:
    #         raise ValidationError('ISBN должен содержать 13 цифр')
    #     return isbn


    # title = models.CharField(max_length=255)
    # author = models.ForeignKey(Author
    # translator = models.ForeignKey(Translator,
    # publisher = models.ForeignKey(Publisher,
    # isbn = models.CharField(
    # year = models.PositiveIntegerField(
    # short_description = models.TextField(
    # key_words = models.TextField(
    # available = models.BooleanField(default=True)  # доступна ли для выдачи
    # times_of_issued = models.PositiveIntegerField(default=0)  # сколько раз выдана книга