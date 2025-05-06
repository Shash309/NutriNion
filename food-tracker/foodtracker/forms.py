from django import forms

from .models import Food


class FoodForm(forms.ModelForm):
    '''
    A ModelForm class for adding a new food item
    '''
    class Meta:
        model = Food
        fields = ['food_name', 'category', 'calories', 'protein', 'fat', 'carbohydrates', 'quantity']

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
