"""
Unit tests for the Enhancement Two weighted scoring algorithm.

No database or dashboard needed. Run from the project folder:
    python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scoring_algorithm import MIN_SCORE, rescue_profiles, score_animal, score_animal_for_profile

WATER_BREEDS = ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']


def dog(breed, sex, weeks):
    return {'breed': breed, 'sex_upon_outcome': sex, 'age_upon_outcome_in_weeks': weeks}


class ScoreAnimalTests(unittest.TestCase):
    """Every test uses the Water Rescue criteria: WATER_BREEDS, Intact Female, ages 26-156."""

    def score(self, animal):
        return score_animal(animal, WATER_BREEDS, 'Intact Female', 26, 156)

    def test_perfect_match_scores_100(self):
        self.assertEqual(self.score(dog('Labrador Retriever Mix', 'Intact Female', 100)), 100)

    def test_breed_and_age_without_sex_reaches_min_score(self):
        # 40 breed + 0 sex + 30 age = 70, which is the cutoff, so the dog is shown
        score = self.score(dog('Newfoundland', 'Intact Male', 100))
        self.assertEqual(score, 70)
        self.assertGreaterEqual(score, MIN_SCORE)

    def test_breed_and_wrong_sex_with_age_off_by_5_weeks_is_hidden(self):
        # 40 + 0 + (30 - 5) = 65, below the cutoff
        score = self.score(dog('Newfoundland', 'Intact Male', 21))
        self.assertEqual(score, 65)
        self.assertLess(score, MIN_SCORE)

    def test_right_sex_and_age_without_breed_is_hidden(self):
        # 0 + 30 + 30 = 60, below the cutoff: a breed match is required to reach 70
        score = self.score(dog('German Shepherd', 'Intact Female', 100))
        self.assertEqual(score, 60)
        self.assertLess(score, MIN_SCORE)

    def test_breed_alone_scores_only_40(self):
        # breed in list, wrong sex, age far outside the range: 40 + 0 + 0
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Male', 1000)), 40)

    def test_age_penalty_stops_at_zero(self):
        # breed + sex = 70 even when age is far outside the range (age points floor at 0)
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Female', 1000)), 70)

    def test_age_boundaries(self):
        # inside the range (inclusive) gets full age points
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Female', 26)), 100)
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Female', 156)), 100)
        # one week outside each bound loses one point
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Female', 25)), 99)
        self.assertEqual(self.score(dog('Newfoundland', 'Intact Female', 157)), 99)

    def test_missing_age_earns_no_age_points(self):
        # Documents current behavior: a NaN age gives 0 age points, with no warning.
        # Decide whether this is the behavior you want, then change the code or this test.
        score = self.score(dog('Newfoundland', 'Intact Female', float('nan')))
        self.assertEqual(score, 70)


class ScoreForProfileTests(unittest.TestCase):
    def test_same_dog_scores_differently_per_profile(self):
        shepherd = dog('German Shepherd', 'Intact Male', 150)
        self.assertEqual(score_animal_for_profile(shepherd, 'Mountain Rescue'), 100)
        self.assertEqual(score_animal_for_profile(shepherd, 'Water Rescue'), 30)

    def test_disaster_profile_uses_wider_age_range(self):
        # Disaster Rescue allows 20-300 weeks, so 300 is in range and 301 loses a point
        self.assertEqual(score_animal_for_profile(dog('Doberman Pinscher', 'Intact Male', 300), 'Disaster Rescue'), 100)
        self.assertEqual(score_animal_for_profile(dog('Doberman Pinscher', 'Intact Male', 301), 'Disaster Rescue'), 99)

    def test_every_profile_has_a_perfect_score_of_100(self):
        # Checks that each profile's weights add up to 100
        for name, profile in rescue_profiles.items():
            with self.subTest(profile=name):
                midpoint = (profile['min_age'] + profile['max_age']) // 2
                animal = dog(profile['breeds'][0], profile['sex'], midpoint)
                self.assertEqual(score_animal_for_profile(animal, name), 100)


if __name__ == "__main__":
    unittest.main()
