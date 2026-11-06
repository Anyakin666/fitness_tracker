def calculate_calories(profile):
    #Миффлин-Сан Жеор
    # Мужчины BMR = 10 × масса (кг) + 6.25 × рост (см) − 5 × возраст (лет) + 5
    # Женщины BMR = 10 × масса (кг) + 6.25 × рост (см) − 5 × возраст (лет) − 161

    if profile.gender == 'male':
        bmr = 10 * float(profile.weight) + 6.25 * profile.height - 5 * profile.age + 5
    else:
        bmr = 10 * float(profile.weight) + 6.25 * profile.height - 5 * profile.age - 161

    # коэфф  активности
    activity_coefficients = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9,
    }
    tdee = bmr * activity_coefficients.get(profile.activity, 1.55)

    # цель
    if profile.goal == 'lose':
        return round(tdee * 0.8)   # дефицит 20%
    elif profile.goal == 'gain':
        return round(tdee * 1.15)  # профицит 15%
    return round(tdee)             # поддержание