from django.shortcuts import render, redirect
from .models import Car
from .forms import CarDataForm, CarAddForm
from django.http import HttpResponseForbidden
from django.contrib.staticfiles import finders
from django.utils import timezone
import json
from static.scripts import parser
import requests
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def add_car(request):
    form = CarAddForm()

    # Добавление введенной информации в БД
    if request.method == 'POST':
        form = CarAddForm(request.POST)
        if form.is_valid():
            vin_number = form.cleaned_data['vin']
            if not Car.objects.filter(vin=vin_number, owner=request.user).exists():
                parsed_data = parser.parse(vin_number)
                
                car = Car.objects.create(
                    vin=vin_number,
                    owner=request.user,
                    number=parsed_data['number'],
                    color=parsed_data['color'],
                    release_year=parsed_data['release_year'],
                    brand=parsed_data['brand'],
                )

                if parsed_data['image'] != '':
                    car.image.save(f'{vin_number}.jpg', BytesIO(requests.get(parsed_data['image']).content))
                    car.save()
            else:
                car = Car.objects.get(vin=vin_number, owner=request.user)

            return redirect('car_data_edit', car.id)

    return render(request, 'add_car.html', {'form': form})


def car_data_edit(request, car_id):
    # Проверка существования машины в БД
    if not Car.objects.filter(id=car_id, owner=request.user).exists():
        return HttpResponseForbidden()
 
    car = Car.objects.get(id=car_id)

    form = CarDataForm(
        initial={
            'number': car.number,
            'color': car.color,
            'release_year': car.release_year,
            'brand': car.brand,
            'current_mileage': car.current_mileage,
            'last_inspection_mileage': car.last_inspection_mileage,
            'daily_mileage': car.daily_mileage,
            'usage_conditions': car.usage_conditions,
            'driving_style': car.driving_style,
            'usage_type': car.usage_type,
            'last_inspection_date': car.last_inspection_date,
            'image': car.image
        }
    )

    # Добавление введенной информации в БД
    if request.method == 'POST':
        form = CarDataForm(request.POST, request.FILES)
        if form.is_valid():
            car.number = form.cleaned_data['number']
            car.color = form.cleaned_data['color']
            car.release_year = form.cleaned_data['release_year']
            car.brand = form.cleaned_data['brand']
            car.current_mileage = form.cleaned_data['current_mileage']
            car.last_inspection_mileage = form.cleaned_data['last_inspection_mileage']
            car.daily_mileage = form.cleaned_data['daily_mileage']
            car.usage_conditions = form.cleaned_data['usage_conditions']
            car.driving_style = form.cleaned_data['driving_style']
            car.usage_type = form.cleaned_data['usage_type']
            car.last_inspection_date = form.cleaned_data['last_inspection_date']

            if 'image' in request.FILES:
                car.image = request.FILES['image']

            car.save()
            return redirect('profile_view')

    return render(request, 'car_data_edit.html', {'car': car, 'form': form})


def car_quiz(request, car_id):
    if not Car.objects.filter(id=car_id, owner=request.user).exists():
        return HttpResponseForbidden()
    car = Car.objects.get(id=car_id)

    if request.method == 'POST':
        json_path = finders.find('json/weights.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            weights = json.load(f)
        
        for key, value in weights.items():
            weights[key] = value['weight'] * value[car.usage_conditions] * value[car.driving_style] * value[car.usage_type]
        
        total_weight = sum(weights.values())
        for key, value in weights.items():
            weights[key] = value / total_weight

        mil_factor = (50 - min(30, car.current_mileage / 250000 * 30) - min(20, (car.current_mileage - car.last_inspection_mileage) / 25000 * 20)) * 0.5
        serv_factor = (30 - min(20, (timezone.now() - car.last_inspection_date).days / 400 * 20)) * 0.3

        car.oil = mil_factor + serv_factor + 0.2 * min(20, (int(request.POST.get('oil_change')) + int(request.POST.get('oil_filter_change')) + int(request.POST.get('oil_leak'))) * weights['engine'] / 3)
        car.oil_filter = mil_factor + serv_factor + 0.2 * min(20, (int(request.POST.get('oil_filter'))))
        car.belt = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('belt_age')) + int(request.POST.get('belt_condition'))) * weights['engine'] / 2))
        car.transmission = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('transmission_oil')) + int(request.POST.get('transmission_problems'))) * weights['transmission'] / 2))
        car.air_filter = mil_factor + serv_factor + 0.2 * min(20, (int(request.POST.get('air_filter')) * weights['filters']))
        car.cabin_filter = mil_factor + serv_factor + 0.2 * min(20, (int(request.POST.get('cabin_filter'))* weights['filters']))
        car.fuel_filter = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('fuel_filter_age')) + int(request.POST.get('fuel_consumption'))) * weights['filters'] / 2))
        car.coolant = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('coolant_age')) + int(request.POST.get('coolant_level'))) * weights['fluids'] / 2))
        car.spark_plugs = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('spark_plugs_age')) + int(request.POST.get('starting_problems'))) * weights['ignition'] / 2))
        car.brake_fluid = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('brake_fluid_age')) + int(request.POST.get('brake_pedal'))) * weights['fluids'] / 2))
        car.brakes = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('brakes_age')) + int(request.POST.get('brake_noise'))) * weights['brakes'] / 2))
        car.shocks = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('shocks_age')) + int(request.POST.get('shocks_condition'))) * weights['suspension'] / 2))
        car.steering = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('steering_play')) + int(request.POST.get('steering_vibration'))) * weights['steering'] / 2))
        car.battery = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('battery_age')) + int(request.POST.get('battery_problems'))) * weights['electrical'] / 2))
        car.tires = mil_factor + serv_factor + 0.2 * min(20, ((int(request.POST.get('tread_depth')) + int(request.POST.get('tire_balance'))) * weights['tires'] / 2))

        car.quiz_date = timezone.now()

        car.save()

        return redirect('car_page', car_id)

    return render(request, 'car_quiz.html')


def car_page(request, car_id):
    if not Car.objects.filter(id=car_id, owner=request.user).exists():
        return HttpResponseForbidden()
    car = Car.objects.get(id=car_id)

    k_json_path = finders.find('json/k_coefficients.json')
    with open(k_json_path, 'r', encoding='utf-8') as f:
        k_coefficients = json.load(f)

    service_json_path = finders.find('json/service_intervals.json')
    with open(service_json_path, 'r', encoding='utf-8') as f:
        service_data = json.load(f)
    
    # Расчет данных компонентов
    if car.quiz_date != None:
        components = []
        deltaP = car.current_mileage - car.last_inspection_mileage
        k = k_coefficients[car.usage_conditions] * k_coefficients[car.driving_style] * k_coefficients[car.usage_type]
        for name, data in service_data.items():
            b_with_time = getattr(car, name) - car.daily_mileage * data['wear'] * (timezone.now() - car.quiz_date).days
            r_expected = round(data['standard_resource'] * (b_with_time / 100))
            r_adjusted = round((r_expected - deltaP) * k)

            priority = 'immediately' if r_adjusted <= 0 or b_with_time < 40 \
                        else 'hight' if r_adjusted <= 500 or b_with_time < 60 \
                        else 'medium' if r_adjusted <= 2000 or b_with_time < 80 \
                        else 'low'

            components.append({
                'name': data['description'],
                'expected': r_expected,
                'current': r_expected - r_adjusted,
                'percent': (r_expected - r_adjusted) / r_expected * 100,
                'priority': priority
                }
            )
    else:
        components = None

    return render(request, 'car_page.html', {'components': components, 'rating': 95, 'car': car})


def car_list(request):
    cars = Car.objects.filter(owner=request.user).order_by('number')
    return render(request, 'my_cars.html', {'cars': cars})


@require_POST
def delete_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id, owner=request.user)
        car.delete()
        return JsonResponse({'success': True})
    except Car.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Автомобиль не найден'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
