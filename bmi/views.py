from django.shortcuts import render

def home(request):
    context = {}

    if request.method == "POST":
        try:
            weight = float(request.POST.get("weight"))
            height_cm = float(request.POST.get("height"))
            height_m = height_cm / 100

            bmi = round(weight / (height_m ** 2), 2)

            if bmi < 18.5:
                category = "Underweight"
                calorie_adjustment = 300
            elif bmi < 25:
                category = "Normal"
                calorie_adjustment = 0
            elif bmi < 30:
                category = "Overweight"
                calorie_adjustment = -300
            else:
                category = "Obese"
                calorie_adjustment = -500

            base_calories = weight * 30
            recommended_calories = int(base_calories + calorie_adjustment)

            context = {
                "bmi": bmi,
                "category": category,
                "calorie_adjustment": recommended_calories
            }

        except Exception:
            context = {
                "error": "Please enter valid numbers"
            }

    return render(request, "bmi/home.html", context)