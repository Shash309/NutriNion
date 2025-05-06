from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from foodtracker.models import FoodCategory, Food, FoodLog

class Command(BaseCommand):
    help = 'Seed the database with initial food categories, food items, and food logs.'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            FoodCategory.objects.get_or_create(category_name='Fruits')[0],
            FoodCategory.objects.get_or_create(category_name='Vegetables')[0],
            FoodCategory.objects.get_or_create(category_name='Grains')[0],
        ]

        # Create foods
        foods = [
            Food.objects.get_or_create(
                food_name='Apple', quantity=150, calories=80, fat=0.3, carbohydrates=21, protein=0.4, category=categories[0]
            )[0],
            Food.objects.get_or_create(
                food_name='Banana', quantity=120, calories=105, fat=0.4, carbohydrates=27, protein=1.3, category=categories[0]
            )[0],
            Food.objects.get_or_create(
                food_name='Carrot', quantity=100, calories=41, fat=0.2, carbohydrates=10, protein=0.9, category=categories[1]
            )[0],
            Food.objects.get_or_create(
                food_name='Broccoli', quantity=91, calories=31, fat=0.3, carbohydrates=6, protein=2.5, category=categories[1]
            )[0],
            Food.objects.get_or_create(
                food_name='Rice', quantity=200, calories=260, fat=0.4, carbohydrates=57, protein=5.2, category=categories[2]
            )[0],
        ]

        # Get a user for food logs
        User = get_user_model()
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.WARNING('No superuser found. Please create a superuser first.'))
            return

        # Create food logs
        FoodLog.objects.get_or_create(user=user, food_consumed=foods[0])
        FoodLog.objects.get_or_create(user=user, food_consumed=foods[2])

        self.stdout.write(self.style.SUCCESS('Seed data added successfully!')) 