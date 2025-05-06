import requests

NUTRITIONIX_API_KEY = 'c65bfb15520c4e8aaad1602f64f081ad'
NUTRITIONIX_APP_ID = '069c7036'

def get_food_nutrition(food_name):
    """
    Fetch nutritional information for a food item from Nutritionix API
    """
    headers = {
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_API_KEY,
        'Content-Type': 'application/json'
    }
    
    data = {
        'query': food_name,
        'timezone': 'US/Eastern'
    }
    
    try:
        response = requests.post(
            'https://trackapi.nutritionix.com/v2/natural/nutrients',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get('foods'):
            food_data = result['foods'][0]
            return {
                'food_name': food_data.get('food_name'),
                'calories': food_data.get('nf_calories'),
                'protein': food_data.get('nf_protein),
                'fat': food_data.get('nf_total_fat'),
                'carbohydrates': food_data.get('nf_total_carbohydrate'),
                'quantity': food_data.get('serving_weight_grams', 100)
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Nutritionix: {e}")
        return None
    
    return None 