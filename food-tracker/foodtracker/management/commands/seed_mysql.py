from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from foodtracker.models import (
    User, IoTDevice, DeviceData, Food, FoodLog, ExerciseLog,
    UserActivityLevel, UserGoal, DailyCalorieIntake, UserCalorieSummary,
    AIRecommendation
)


class Command(BaseCommand):
    help = 'Seed the database with initial data for MySQL schema'

    def handle(self, *args, **kwargs):
        # Create users
        user1 = User.objects.create_user(
            username='SwastikPandey',
            email='swastik@example.com',
            password='hashedpassword123',
            age=20,
            gender='Male',
            weight=68,
            height=179
        )

        user2 = User.objects.create_user(
            username='ShashwatSharma',
            email='shashwat@example.com',
            password='hashedpassword456',
            age=20,
            gender='Male',
            weight=72,
            height=178
        )

        # Create IoT devices
        device1 = IoTDevice.objects.create(
            user=user1,
            device_type='Smartwatch',
            status='Active'
        )

        device2 = IoTDevice.objects.create(
            user=user2,
            device_type='Fitness Band',
            status='Inactive'
        )

        # Create device data
        DeviceData.objects.create(
            device=device1,
            heart_rate=75,
            steps=8000,
            sleep_duration=7.5,
            calories_burned=200
        )

        DeviceData.objects.create(
            device=device2,
            heart_rate=80,
            steps=10000,
            sleep_duration=8.0,
            calories_burned=300
        )

        # Create food items
        apple = Food.objects.create(
            name='Apple',
            calories=52,
            protein=0.3,
            fats=0.2,
            carbs=14,
            serving_size='100 gm'
        )

        banana = Food.objects.create(
            name='Banana',
            calories=89,
            protein=1.1,
            fats=0.3,
            carbs=23,
            serving_size='100 gm'
        )

        # Create food logs
        FoodLog.objects.create(
            user=user1,
            food=apple,
            nutrients_info='Nutrients: Calories: 52, Protein: 0.3g, Fats: 0.2g'
        )

        FoodLog.objects.create(
            user=user2,
            food=banana,
            nutrients_info='Nutrients: Calories: 89, Protein: 1.1g, Fats: 0.3g'
        )

        # Create exercise logs
        ExerciseLog.objects.create(
            user=user1,
            exercise_name='Running',
            duration=30,
            calories_burned=300
        )

        ExerciseLog.objects.create(
            user=user2,
            exercise_name='Cycling',
            duration=45,
            calories_burned=400
        )

        # Create activity levels
        UserActivityLevel.objects.create(
            user=user1,
            activity_level='Moderate'
        )

        UserActivityLevel.objects.create(
            user=user2,
            activity_level='High'
        )

        # Create goals
        UserGoal.objects.create(
            user=user1,
            goal='Lose 5 kg in 2 months'
        )

        UserGoal.objects.create(
            user=user2,
            goal='Gain 3 kg in 1 month'
        )

        # Create daily calorie intake
        DailyCalorieIntake.objects.create(
            user=user1,
            total_calories=2500
        )

        DailyCalorieIntake.objects.create(
            user=user2,
            total_calories=2300
        )

        # Create calorie summaries
        UserCalorieSummary.objects.create(
            user=user1,
            age=20,
            height=179,
            weight=68,
            total_calories=2500
        )

        UserCalorieSummary.objects.create(
            user=user2,
            age=20,
            height=178,
            weight=72,
            total_calories=2300
        )

        # Create AI recommendations
        AIRecommendation.objects.create(
            user=user1,
            recommendation_text='Increase protein intake to boost muscle recovery'
        )

        AIRecommendation.objects.create(
            user=user2,
            recommendation_text='Try to get 30 minutes of activity every day'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded MySQL data!')) 