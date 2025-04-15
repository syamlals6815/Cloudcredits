from django.shortcuts import render, redirect
from .forms import BMIForm

def index(request):
    return render(request, 'calculator/index.html')

def calculate_bmi(request):
    height_m = None  # Prevent UnboundLocalError
    height_in = None

    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            unit_system = form.cleaned_data['unit_system']
            
            # Calculate BMI based on unit system
            if unit_system == 'metric':
                weight = form.cleaned_data['weight_kg']
                height = form.cleaned_data['height_m']
                bmi = weight / (height ** 2)
            else:  # Imperial system
                weight = form.cleaned_data['weight_lbs']
                height_ft = form.cleaned_data['height_ft']
                height_in = form.cleaned_data.get('height_in', 0)
                
                # Convert height to meters
                # 1 foot = 0.3048 meters, 1 inch = 0.0254 meters
                height_m = (height_ft * 0.3048) + (height_in * 0.0254)
                
                # Convert weight to kg (1 lb = 0.453592 kg)
                weight_kg = weight * 0.453592
                
                # Calculate BMI
                bmi = weight_kg / (height_m ** 2)
            
            # Round BMI to 1 decimal place
            bmi = round(bmi, 1)
            
            # Calculate indicator position for the BMI scale
            # Cap the BMI value to a reasonable range (15-45) for positioning
            capped_bmi = max(15, min(45, bmi))
            # Calculate position percentage (15 to 45 BMI range mapped to 0-100%)
            indicator_position = ((capped_bmi - 15) / 30) * 100
            
            # Determine BMI category
            if bmi < 18.5:
                category = 'Underweight'
                description = 'You may need to gain some weight. Consider consulting with a healthcare professional.'
                image = 'underweight.png'
            elif 18.5 <= bmi < 25:
                category = 'Normal Weight'
                description = 'You have a healthy weight. Maintain your current lifestyle with regular exercise and a balanced diet.'
                image = 'normalweight.png'
            elif 25 <= bmi < 30:
                category = 'Overweight'
                description = 'You may benefit from losing some weight. Focus on healthy eating and regular physical activity.'
                image = 'overweight.png'
            else:  # bmi >= 30
                category = 'Obese'
                description = 'Your health may be at risk. Consider consulting with a healthcare professional about weight management.'
                image = 'obese.png'
            
            context = {
                'bmi': bmi,
                'category': category,
                'description': description,
                'image': image,
                'weight': weight,
                'height': height_m if unit_system == 'metric' else height_ft,
                'height_in': height_in if unit_system == 'imperial' else None,
                'unit_system': unit_system,
                'indicator_position': indicator_position,  # Add this to the context
            }
            
            return render(request, 'calculator/result.html', context)
        
    else:
        form = BMIForm()
    
    return render(request, 'calculator/index.html', {'form': form})