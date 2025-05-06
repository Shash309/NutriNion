from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class IoTDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ])

    def __str__(self):
        return f'{self.device_type} - {self.status}'


class DeviceData(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.IntegerField()
    steps = models.IntegerField()
    sleep_duration = models.FloatField()
    calories_burned = models.FloatField()

    def __str__(self):
        return f'Device Data - {self.timestamp}'


class Food(models.Model):
    food_name = models.CharField(max_length=100)
    category = models.ForeignKey('FoodCategory', on_delete=models.CASCADE, related_name='foods', null=True, blank=True)
    calories = models.IntegerField(default=0)
    protein = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)
    carbohydrates = models.FloatField(default=0.0)
    quantity = models.FloatField(default=100.0)  # in grams

    def __str__(self):
        return f'{self.food_name}'


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    consumed_at = models.DateTimeField(auto_now_add=True)
    nutrients_info = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.food.food_name}'


class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.FloatField()

    def __str__(self):
        return f'{self.user.username} - {self.exercise_name}'


class UserActivityLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_level = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.activity_level}'


class UserGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.goal}'


class DailyCalorieIntake(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    total_calories = models.DecimalField(max_digits=32, decimal_places=0)

    def __str__(self):
        return f'{self.user.username} - {self.total_calories} calories'


class UserCalorieSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    total_calories = models.DecimalField(max_digits=32, decimal_places=0)

    def __str__(self):
        return f'{self.user.username} - Summary'


class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    recommendation_text = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'


class FoodCategory(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_food_by_category(self):
        return Food.objects.filter(category=self).count()


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weight'

    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.entry_date}'
