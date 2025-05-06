from django.core.management.base import BaseCommand
from foodtracker.models import FoodCategory, Food
from foodtracker.utils import get_food_nutrition

class Command(BaseCommand):
    help = 'Seeds the database with initial food categories and food items'

    def handle(self, *args, **options):
        # Create food categories
        categories = [
            'Fruits',
            'Vegetables',
            'Grains',
            'Proteins',
            'Dairy',
            'Snacks',
            'Beverages'
        ]

        for category_name in categories:
            FoodCategory.objects.get_or_create(category_name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))

        # Create food items
        foods = [
            # Fruits
            {'food_name': 'Apple', 'category': 'Fruits', 'query': '1 medium apple'},
            {'food_name': 'Banana', 'category': 'Fruits', 'query': '1 medium banana'},
            {'food_name': 'Mango', 'category': 'Fruits', 'query': '1 medium mango'},
            {'food_name': 'Orange', 'category': 'Fruits', 'query': '1 medium orange'},
            # Vegetables
            {'food_name': 'Carrot', 'category': 'Vegetables', 'query': '100g raw carrot'},
            {'food_name': 'Spinach', 'category': 'Vegetables', 'query': '100g raw spinach'},
            {'food_name': 'Broccoli', 'category': 'Vegetables', 'query': '100g raw broccoli'},
            {'food_name': 'Potato', 'category': 'Vegetables', 'query': '100g boiled potato'},
            # Grains
            {'food_name': 'Brown Rice', 'category': 'Grains', 'query': '100g cooked brown rice'},
            {'food_name': 'Chapati', 'category': 'Grains', 'query': '1 medium chapati'},
            {'food_name': 'Oats', 'category': 'Grains', 'query': '40g rolled oats'},
            {'food_name': 'Quinoa', 'category': 'Grains', 'query': '100g cooked quinoa'},
            # Proteins
            {'food_name': 'Chicken Breast', 'category': 'Proteins', 'query': '100g grilled chicken breast'},
            {'food_name': 'Paneer', 'category': 'Proteins', 'query': '100g paneer'},
            {'food_name': 'Egg', 'category': 'Proteins', 'query': '1 large egg'},
            {'food_name': 'Tofu', 'category': 'Proteins', 'query': '100g tofu'},
            # Dairy
            {'food_name': 'Milk', 'category': 'Dairy', 'query': '100ml whole milk'},
            {'food_name': 'Yogurt', 'category': 'Dairy', 'query': '100g plain yogurt'},
            {'food_name': 'Cheddar Cheese', 'category': 'Dairy', 'query': '30g cheddar cheese'},
            # Snacks
            {'food_name': 'Almonds', 'category': 'Snacks', 'query': '28g raw almonds'},
            {'food_name': 'Samosa', 'category': 'Snacks', 'query': '1 medium samosa'},
            {'food_name': 'Granola Bar', 'category': 'Snacks', 'query': '1 granola bar'},
            # Beverages
            {'food_name': 'Orange Juice', 'category': 'Beverages', 'query': '240ml orange juice'},
            {'food_name': 'Masala Chai', 'category': 'Beverages', 'query': '1 cup masala chai'},
            {'food_name': 'Black Coffee', 'category': 'Beverages', 'query': '1 cup black coffee'},
            # South Indian Foods
            {'food_name': 'Idli', 'category': 'Grains', 'query': '2 medium idli'},
            {'food_name': 'Dosa', 'category': 'Grains', 'query': '1 plain dosa'},
            {'food_name': 'Uttapam', 'category': 'Grains', 'query': '1 medium uttapam'},
            {'food_name': 'Sambar', 'category': 'Vegetables', 'query': '1 cup sambar'},
            {'food_name': 'Coconut Chutney', 'category': 'Vegetables', 'query': '2 tbsp coconut chutney'},
            {'food_name': 'Medu Vada', 'category': 'Snacks', 'query': '1 medu vada'},
            {'food_name': 'Pongal', 'category': 'Grains', 'query': '1 cup pongal'},
            {'food_name': 'Rasam', 'category': 'Vegetables', 'query': '1 cup rasam'},
        ]

        for food_data in foods:
            category = FoodCategory.objects.get(category_name=food_data.pop('category'))
            query = food_data.pop('query')
            
            # Get nutritional data from Nutritionix
            nutrition_data = get_food_nutrition(query)
            if nutrition_data:
                food_data.update(nutrition_data)
                Food.objects.get_or_create(
                    category=category,
                    **food_data
                )
                self.stdout.write(self.style.SUCCESS(f'Created food: {food_data["food_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Failed to get nutrition data for: {food_data["food_name"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database')) 