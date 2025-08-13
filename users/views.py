from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import LoginForm, SignUpForm, ProfileEditForm

class CustomLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html', { 'user': request.user })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'profile_edit.html', { 'form': form })

def car_detail(request, car_id):
    # Логика для отображения деталей конкретной машины
    return render(request, 'cars/detail.html', {'car_id': car_id})

def car_detail(request, car_id):
    car = {
        'id': car_id,
        'name': 'Audi A6',
        'image': 'images/car1.png',
        'color': 'Черный',
        'brand': 'Audi',
    }
    
    components = [
        {'name': 'Моторное масло', 'current': 7500, 'max': 10000, 'icon': 'icons/oil.png'},
        {'name': 'Масляный фильтр', 'current': 15000, 'max': 15000, 'icon': 'icons/filter.png'},
        # ... остальные компоненты
    ]
    
    # Добавляем процент для каждого компонента
    for component in components:
        component['percent'] = min(100, int((component['current'] / component['max']) * 100))
    
    return render(request, 'cars/detail.html', {
        'car': car,
        'components': components
    })

def ai_list(request):
    # Логика для отображения списка машин
    return render(request, 'ai.html')

def service_list(request):
    # Логика для отображения списка машин
    return render(request, 'servise.html')