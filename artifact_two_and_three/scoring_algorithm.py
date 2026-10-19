# Final is not enforced at runtime; static type checkers (e.g., mypy) flag reassignment
from typing import Final
# 70 = breed match plus one other criterion; lower values admit wrong-breed animals
MIN_SCORE: Final = 70

# returns numeric score from 0 - 100; assigns animal a weighted score based on parameters for breed, sex, & min/max age
def score_animal(animal, preferred_breeds, preferred_sex, min_age, max_age):
    # Weight values for breed, sex, age; SUM = 100
    BREED_WEIGHT = 40
    SEX_WEIGHT = 30
    AGE_WEIGHT = 30

    score = 0

    # BREED_WEIGHT if preferred breed, else 0
    if animal['breed'] in preferred_breeds:
        score += BREED_WEIGHT
    
    # SEX_WEIGHT if preferred sex, else 0
    if animal['sex_upon_outcome'] == preferred_sex:
        score += SEX_WEIGHT

    # full credit inside the range; outside it, lose 1 point per week from the nearest bound (minimum 0)
    age = animal['age_upon_outcome_in_weeks']
    if min_age <= age <= max_age:
        score += AGE_WEIGHT
    else:
        if age < min_age:
            distance = min_age - age
        else:
            distance = age - max_age
        score += max(0, AGE_WEIGHT - distance)

    return score

#########################################
# DEBUG: score_animal
# Uncomment below for debugging score_animal()
#
# test_animals = [
#     {'breed': 'Labrador Retriever Mix', 'sex_upon_outcome': 'Intact Female', 'age_upon_outcome_in_weeks': 100},
#     {'breed': 'Labrador Retriever Mix', 'sex_upon_outcome': 'Intact Male', 'age_upon_outcome_in_weeks': 100},
#     {'breed': 'Chihuahua', 'sex_upon_outcome': 'Intact Female', 'age_upon_outcome_in_weeks': 160},
# ]
#
# water_rescue_breeds = ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']
#
# for animal in test_animals:
#     result = score_animal(animal, water_rescue_breeds, 'Intact Female', 26, 156)
#     print(f"{animal['breed']}, {animal['sex_upon_outcome']}, {animal['age_upon_outcome_in_weeks']} weeks -> score: {result}")

# dictionary holds search criteria specifications for each type of rescue profile
rescue_profiles = {
    'Water Rescue': {
        'breeds': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland'],
        'sex': 'Intact Female',
        'min_age': 26,
        'max_age': 156
    },
    'Mountain Rescue': {
        'breeds': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler'],
        'sex': 'Intact Male',
        'min_age': 26,
        'max_age': 156
    },
    'Disaster Rescue': {
        'breeds': ['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler'],
        'sex': 'Intact Male',
        'min_age': 20,
        'max_age': 300
    }
}

# returns numeric score from 0 - 100; scores animal based on breed, sex, and age criteria defined in the rescue_profiles dictionary
def score_animal_for_profile(animal, profile_name):
    profile = rescue_profiles[profile_name]
    return score_animal(animal, profile['breeds'], profile['sex'], profile['min_age'], profile['max_age'])

################################################
# DEBUG: score_animal_for_profile
# Uncomment debug sections above AND below for debugging score_animal_for_profile()
#
# test_animals.append(
#     {'breed': 'German Shepherd', 'sex_upon_outcome': 'Intact Male', 'age_upon_outcome_in_weeks': 80}
# )
#
# for profile_name in rescue_profiles:
#     print(f"--- {profile_name} ---")
#     for animal in test_animals:
#         result = score_animal_for_profile(animal, profile_name)
#         print(f"{animal['breed']}, {animal['sex_upon_outcome']}, {animal['age_upon_outcome_in_weeks']} weeks -> score: {result}")
#
# import pandas as pd
# from animal_shelter import AnimalShelter
#
# db = AnimalShelter()
# df = pd.DataFrame.from_records(db.read({}))
#
# df['fit_score'] = df.apply(lambda row: score_animal_for_profile(row, 'Water Rescue'), axis=1)
#
# ranked_df = df.sort_values('fit_score', ascending=False)
#
# print(ranked_df[['breed', 'sex_upon_outcome', 'age_upon_outcome_in_weeks', 'fit_score']].tail(10))

