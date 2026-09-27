from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import (
    SessionLocal,
    User,
    WorkoutPlan,
    NutritionPlan,
    Feedback,
    WellnessTip
)

from .ai import (
    generate_workout_gemini,
    generate_nutrition_gemini,
    generate_updated_plan,
    generate_wellness_tip
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================
# HOME
# =========================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================
# WORKOUT GENERATION
# =========================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
async def generate_workout(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    db = SessionLocal()
    user = None

    try:

        user = User(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        plan_text = generate_workout_gemini(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        plan = WorkoutPlan(
            user_id=user.id,
            plan_text=plan_text
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan,
                "error": None
            }
        )

    except Exception as e:

        db.rollback()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": None,
                "error": str(e)
            }
        )

    finally:

        db.close()


# =========================
# NUTRITION
# =========================

@router.get(
    "/nutrition",
    response_class=HTMLResponse
)
async def nutrition_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="nutrition.html",
        context={}
    )


@router.post(
    "/generate-nutrition",
    response_class=HTMLResponse
)
async def generate_nutrition(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    preferences: str = Form("")
):

    db = SessionLocal()

    try:

        nutrition_text = generate_nutrition_gemini(
            name=name,
            age=age,
            goal=goal,
            preferences=preferences
        )

        return templates.TemplateResponse(
            request=request,
            name="nutrition_result.html",
            context={
                "nutrition": nutrition_text,
                "error": None
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="nutrition_result.html",
            context={
                "nutrition": None,
                "error": str(e)
            }
        )

    finally:

        db.close()


# =========================
# FEEDBACK
# =========================

@router.get(
    "/feedback",
    response_class=HTMLResponse
)
async def feedback_page(request: Request):

    db = SessionLocal()

    try:

        users = db.query(User).all()

        return templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={
                "users": users
            }
        )

    finally:

        db.close()


@router.post(
    "/feedback",
    response_class=HTMLResponse
)
async def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback_text: str = Form(...)
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:

            return templates.TemplateResponse(
                request=request,
                name="updated_plan.html",
                context={
                    "error": "User not found.",
                    "updated_plan": None
                }
            )

        latest_plan = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user_id)
            .order_by(WorkoutPlan.id.desc())
            .first()
        )

        if not latest_plan:

            return templates.TemplateResponse(
                request=request,
                name="updated_plan.html",
                context={
                    "error": "No workout plan found.",
                    "updated_plan": None
                }
            )

        updated_plan = generate_updated_plan(
            user=user,
            current_plan=latest_plan.plan_text,
            feedback_text=feedback_text
        )

        feedback = Feedback(
            user_id=user_id,
            feedback_text=feedback_text,
            updated_plan=updated_plan
        )

        db.add(feedback)

        new_plan = WorkoutPlan(
            user_id=user_id,
            plan_text=updated_plan
        )

        db.add(new_plan)
        db.commit()

        return templates.TemplateResponse(
            request=request,
            name="updated_plan.html",
            context={
                "user": user,
                "updated_plan": updated_plan,
                "error": None
            }
        )

    except Exception as e:

        db.rollback()

        return templates.TemplateResponse(
            request=request,
            name="updated_plan.html",
            context={
                "user": None,
                "updated_plan": None,
                "error": str(e)
            }
        )

    finally:

        db.close()


# =========================
# WELLNESS TIPS
# =========================

@router.get(
    "/tips",
    response_class=HTMLResponse
)
async def tips_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="tips.html",
        context={}
    )


@router.post(
    "/generate-tip",
    response_class=HTMLResponse
)
async def generate_tip(
    request: Request,
    tip_type: str = Form(...)
):

    try:

        tip = generate_wellness_tip(
            tip_type
        )

        return templates.TemplateResponse(
            request=request,
            name="tips.html",
            context={
                "tip": tip,
                "error": None
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="tips.html",
            context={
                "tip": None,
                "error": str(e)
            }
        )


# =========================
# DASHBOARD
# =========================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request
):

    db = SessionLocal()

    try:

        users = db.query(User).all()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "users": users
            }
        )

    finally:

        db.close()


# =========================
# VIEW ALL USERS
# =========================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
async def view_all_users(
    request: Request
):

    db = SessionLocal()

    try:

        users = db.query(User).all()

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "users": users
            }
        )

    finally:

        db.close()