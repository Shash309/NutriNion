from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Food, FoodCategory, FoodLog, Weight
from .forms import FoodForm


def index(request):
    '''
    The default route which lists all food items
    '''
    return food_list_view(request)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST.get('gender')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        age = request.POST.get('age')

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': FoodCategory.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.gender = gender
            user.height = height
            user.weight = weight
            user.age = age
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'categories': FoodCategory.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html', {
            'categories': FoodCategory.objects.all()
        })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html',  {
            'categories': FoodCategory.objects.all()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def food_list_view(request):
    '''
    It renders a page that displays all food items
    Food items are paginated: 8 per page
    '''
    foods = Food.objects.all()

    # Show 8 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 8)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })


def food_details_view(request, food_id):
    '''
    It renders a page that displays the details of a selected food item
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
    })


@login_required
def food_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    if request.method == 'POST':
        food_form = FoodForm(request.POST)
        if food_form.is_valid():
            food_form.save()
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'success': True
            })
        else:
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
            })
    else:
        return render(request, 'food_add.html', {
            'categories': FoodCategory.objects.all(),
            'food_form': FoodForm(),
        })


@login_required
def food_log_view(request):
    '''
    It allows the user to select food items and
    add them to their food log
    '''
    if request.method == 'POST':
        foods = Food.objects.all()

        # get the food item selected by the user
        food = request.POST['food_consumed']
        # Use filter().first() instead of get() to handle multiple items with same name
        food_consumed = Food.objects.filter(food_name=food).first()

        if food_consumed:
            # get the currently logged in user
            user = request.user

            # create nutrients_info string
            nutrients_info = f"Nutrients: Calories: {food_consumed.calories}, Protein: {food_consumed.protein}g, Fats: {food_consumed.fat}g, Carbs: {food_consumed.carbohydrates}g"

            # add selected food to the food log
            food_log = FoodLog(user=user, food=food_consumed, nutrients_info=nutrients_info)
            food_log.save()

    else:  # GET method
        foods = Food.objects.all()

    # get the food log of the logged in user
    user_food_log = FoodLog.objects.filter(user=request.user)

    return render(request, 'food_log.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'user_food_log': user_food_log
    })


@login_required
def food_log_delete(request, food_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    food_consumed = FoodLog.objects.filter(id=food_id)

    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')

    return render(request, 'food_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


@login_required
def weight_log_view(request):
    '''
    It allows the user to record their weight
    '''
    if request.method == 'POST':

        # get the values from the form
        weight = request.POST['weight']
        entry_date = request.POST['date']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        weight_log = Weight(user=user, weight=weight, entry_date=entry_date)
        weight_log.save()

    # get the weight log of the logged in user
    user_weight_log = Weight.objects.filter(user=request.user)

    return render(request, 'user_profile.html', {
        'categories': FoodCategory.objects.all(),
        'user_weight_log': user_weight_log
    })


@login_required
def weight_log_delete(request, weight_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    weight_recorded = Weight.objects.filter(id=weight_id)

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')

    return render(request, 'weight_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


def categories_view(request):
    '''
    It renders a list of all food categories
    '''
    return render(request, 'categories.html', {
        'categories': FoodCategory.objects.all()
    })


def category_details_view(request, category_name):
    '''
    Clicking on the name of any category takes the user to a page that
    displays all of the foods in that category
    Food items are paginated: 8 per page
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = FoodCategory.objects.get(category_name=category_name)
    foods = Food.objects.filter(category=category)

    # Show 8 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 8)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })
