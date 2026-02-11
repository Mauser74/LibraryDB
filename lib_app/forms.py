from datetime import datetime

from django import forms


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