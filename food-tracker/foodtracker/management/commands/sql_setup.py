from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Set up MySQL triggers and stored procedures'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Create trigger to check daily meal limit
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS check_meal_limit
                BEFORE INSERT ON foodtracker_foodlog
                FOR EACH ROW
                BEGIN
                    DECLARE daily_calories DECIMAL(32, 0);
                    DECLARE food_calories INT;
                    
                    -- Get the calories of the food being logged
                    SELECT calories INTO food_calories
                    FROM foodtracker_food
                    WHERE id = NEW.food_id;
                    
                    -- Get the user's daily calorie intake
                    SELECT total_calories INTO daily_calories
                    FROM foodtracker_dailycalorieintake
                    WHERE user_id = NEW.user_id;
                    
                    -- Check if adding this food would exceed the daily limit
                    IF daily_calories + food_calories > 3000 THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Daily calorie limit exceeded';
                    END IF;
                END;
            """)

            # Create stored procedure to get high calorie foods
            cursor.execute("""
                CREATE PROCEDURE IF NOT EXISTS GetHighCalorieFoods(IN calorie_threshold INT)
                BEGIN
                    SELECT f.name, f.calories, f.protein, f.fats, f.carbs
                    FROM foodtracker_food f
                    WHERE f.calories > calorie_threshold
                    ORDER BY f.calories DESC;
                END;
            """)

            # Create stored procedure to calculate daily activity summary
            cursor.execute("""
                CREATE PROCEDURE IF NOT EXISTS CalculateDailyActivitySummary(IN user_id_param INT)
                BEGIN
                    SELECT 
                        SUM(dd.steps) as total_steps,
                        AVG(dd.heart_rate) as avg_heart_rate,
                        SUM(dd.calories_burned) as total_calories_burned,
                        AVG(dd.sleep_duration) as avg_sleep_duration
                    FROM foodtracker_devicedata dd
                    JOIN foodtracker_iotdevice id ON dd.device_id = id.id
                    WHERE id.user_id = user_id_param
                    AND DATE(dd.timestamp) = CURDATE();
                END;
            """)

            # Create stored procedure to get user's nutrition summary
            cursor.execute("""
                CREATE PROCEDURE IF NOT EXISTS GetUserNutritionSummary(IN user_id_param INT)
                BEGIN
                    SELECT 
                        SUM(f.calories) as total_calories,
                        SUM(f.protein) as total_protein,
                        SUM(f.fats) as total_fats,
                        SUM(f.carbs) as total_carbs
                    FROM foodtracker_foodlog fl
                    JOIN foodtracker_food f ON fl.food_id = f.id
                    WHERE fl.user_id = user_id_param
                    AND DATE(fl.consumed_at) = CURDATE();
                END;
            """)

        self.stdout.write(self.style.SUCCESS('Successfully created MySQL triggers and stored procedures!')) 