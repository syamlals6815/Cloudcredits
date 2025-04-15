from django import forms

class BMIForm(forms.Form):
    UNIT_CHOICES = [
        ('metric', 'Metric (kg, m)'),
        ('imperial', 'Imperial (lbs, ft)'),
    ]
    
    unit_system = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.RadioSelect,
        initial='metric',
        label='Measurement System'
    )
    
    # Metric fields
    weight_kg = forms.FloatField(
        required=False,
        min_value=20,
        max_value=500,
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Enter weight in kg'})
    )
    height_m = forms.FloatField(
        required=False,
        min_value=0.5,
        max_value=3,
        label='Height (m)',
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter height in meters'})
    )
    
    # Imperial fields
    weight_lbs = forms.FloatField(
        required=False,
        min_value=40,
        max_value=1000,
        label='Weight (lbs)',
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Enter weight in pounds'})
    )
    height_ft = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=8,
        label='Height (ft)',
        widget=forms.NumberInput(attrs={'placeholder': 'Feet'})
    )
    height_in = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=11,
        label='Height (in)',
        widget=forms.NumberInput(attrs={'placeholder': 'Inches'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        unit_system = cleaned_data.get('unit_system')
        
        if unit_system == 'metric':
            weight_kg = cleaned_data.get('weight_kg')
            height_m = cleaned_data.get('height_m')
            
            if not weight_kg:
                self.add_error('weight_kg', 'Please enter your weight in kg')
            if not height_m:
                self.add_error('height_m', 'Please enter your height in meters')
                
        elif unit_system == 'imperial':
            weight_lbs = cleaned_data.get('weight_lbs')
            height_ft = cleaned_data.get('height_ft')
            
            if not weight_lbs:
                self.add_error('weight_lbs', 'Please enter your weight in pounds')
            if not height_ft:
                self.add_error('height_ft', 'Please enter your height (feet)')
        
        return cleaned_data