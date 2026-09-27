import os

from google import genai
from .config import (
    GEMINI_API_KEY,
    WORKOUT_MODEL,
    TIP_MODEL
)


def get_client():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# ==========================================
# WORKOUT PLAN GENERATION
# ==========================================

def generate_workout_gemini(
    name,
    age,
    weight,
    goal,
    intensity
):

    client = get_client()

    prompt = f"""
You are FitBuddy AI, a safe general wellness assistant.

User information:
Name: {name}
Age: {age}
Weight: {weight}
Goal: {goal}
Activity level: {intensity}

Generate a personalized 7-day general wellness activity plan.

Format:

DAY 1
Activity:
Duration:
Instructions:
Recovery:

DAY 2
Activity:
Duration:
Instructions:
Recovery:

Continue through DAY 7.

Also include:
- Warm-up guidance
- Cool-down guidance
- Hydration reminder
- Sleep and recovery guidance

Keep activities safe and age appropriate.

Do not provide extreme exercise,
unsafe challenges, calorie restriction,
or restrictive dieting.

Focus on general health and wellness.
"""

    response = client.models.generate_content(
        model=WORKOUT_MODEL,
        contents=prompt
    )

    return response.text


# ==========================================
# NUTRITION GENERATION
# ==========================================

def generate_nutrition_gemini(
    name,
    age,
    goal,
    preferences
):

    client = get_client()

    prompt = f"""
You are FitBuddy AI, a general wellness assistant.

User information:

Name: {name}
Age: {age}
Goal: {goal}
Food preferences: {preferences}

Create a 7-day healthy eating idea guide.

For each day provide:

DAY 1
Breakfast:
Lunch:
Snack:
Dinner:
Hydration:

Continue through DAY 7.

Use balanced and normal meals.

Include a variety of:
- Vegetables
- Fruits
- Whole grains
- Protein foods
- Dairy or suitable alternatives
- Water

Keep the advice suitable for teenagers and adults.

Do not provide:
- Extreme dieting
- Calorie restriction
- Meal skipping
- Weight-loss targets
- Unsafe nutrition advice

Focus on general wellness and healthy eating habits.
"""

    response = client.models.generate_content(
        model=TIP_MODEL,
        contents=prompt
    )

    return response.text


# ==========================================
# FEEDBACK / UPDATED WORKOUT
# ==========================================

def generate_updated_plan(
    user,
    current_plan,
    feedback_text
):

    client = get_client()

    prompt = f"""
You are FitBuddy AI.

User:
Name: {user.name}
Age: {user.age}
Goal: {user.goal}
Activity level: {user.intensity}

Current workout plan:
{current_plan}

User feedback:
{feedback_text}

Create an updated 7-day general wellness plan
based on the user's feedback.

Keep the activities safe and age appropriate.

Do not provide extreme exercise,
unsafe challenges, or restrictive eating advice.

Clearly organize the updated plan by Day 1 to Day 7.
"""

    response = client.models.generate_content(
        model=WORKOUT_MODEL,
        contents=prompt
    )

    return response.text


# ==========================================
# WELLNESS TIPS
# ==========================================

def generate_wellness_tip(
    tip_type
):

    client = get_client()

    prompt = f"""
You are FitBuddy AI.

Generate a simple general wellness guide about:

{tip_type}

Include:

1. Short explanation
2. Three practical tips
3. One safety reminder

Keep the information suitable for teenagers
and adults.

Do not diagnose or treat medical conditions.
"""

    response = client.models.generate_content(
        model=TIP_MODEL,
        contents=prompt
    )

    return response.text