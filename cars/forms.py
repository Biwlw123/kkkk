from django import forms
from django.core.validators import FileExtensionValidator, MaxValueValidator

class CarAddForm(forms.Form):
    vin = forms.CharField(max_length=17, label="VIN-номер автомобиля")

class CarDataForm(forms.Form):
    number = forms.CharField(max_length=9, label="Госномер")
    color = forms.CharField(max_length=20, label="Цвет")
    release_year = forms.CharField(max_length=4, label="Год выпуска")
    brand = forms.CharField(max_length=20, label="Марка")
    current_mileage = forms.IntegerField(label="Текущий пробег")
    last_inspection_mileage = forms.IntegerField(label="Пробег последнего ТО")
    daily_mileage = forms.IntegerField(label="Средний пробег за день")
    usage_conditions = forms.ChoiceField(
        choices=(
           ('city', 'Город'),
           ('highway', 'Шоссе'),
           ('off-road', 'Бездорожье'),
           ('mixed', 'Смешанный'),
       ),
       label="Условия использования"
    )
    driving_style = forms.ChoiceField(
        choices=(
           ('calm', 'Спокойный'),
           ('universal', 'Универсальный'),
           ('agressive', 'Агрессивный'),
       ),
       label="Стиль вождения"
    )
    usage_type = forms.ChoiceField(
        choices=(
           ('personal', 'Личный'),
           ('taxi', 'Такси'),
           ('rental', 'Прокат'),
           ('delivery', 'Доставка'),
       ),
       label="Тип использования"
    )
    last_inspection_date = forms.DateField(
        label='Дата последнего ТО',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    image = forms.ImageField(
        label='Фотография автомобиля',
        required=False
    )
