from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import authenticate, login, logout
from .models import Topic, CustomUser
from django.middleware.csrf import get_token
from django.shortcuts import redirect


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        # Get data from request body
        data = json.loads(request.body.decode("utf-8"))
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # Check if a user with the given email already exists
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "User with this email already exists."}, status=400
            )

        # Create a new user
        user = CustomUser.objects.create_user(name=name, email=email, password=password)

        if user:
            return JsonResponse({"message": "User registered successfully."})
        else:
            return JsonResponse(
                {"message": "Error occurred during registration."}, status=500
            )

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Get data from request body
        data = json.loads(request.body.decode("utf-8"))
        email = data.get("email")
        password = data.get("password")
        remember_me = data.get("remember_me") == "true"

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    # Session expires when the browser is closed
                    request.session.set_expiry(0)

                return JsonResponse({"message": "Login successful."})
            else:
                return JsonResponse(
                    {"message": "Your account is not active."}, status=403
                )
        else:
            return JsonResponse({"message": "Invalid email or password."}, status=401)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@csrf_exempt
def logout_view(request):
    # Logout the user
    logout(request)
    
    # Delete the authentication cookies
    response = JsonResponse({'message': 'Logout successful.'})
    # response.delete_cookie('your_auth_cookie_name')  # Replace with your actual cookie name
    return response


@csrf_exempt
@require_POST
def update_topics(request):
    user = request.user
    if user.is_authenticated:
        # User is logged in
        data = json.loads(request.body.decode("utf-8")).get("selectedTopics")

        # Get all old topics for the user
        old_topics = user.topics.all()

        # Create a set of new topic names
        new_topic_names = set(data)

        # Update or create topics and track updated topics
        updated_topics = []
        for topic_name in new_topic_names:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            user.topics.add(topic)
            updated_topics.append(topic.name)

        # Delete old topics not in the new list
        for old_topic in old_topics:
            if old_topic.name not in new_topic_names:
                user.topics.remove(old_topic)

        return JsonResponse(
            {
                "message": "Topics updated successfully",
                "updated_topics": updated_topics,
            },
            status=200,
        )
    else:
        # User is not logged in
        return JsonResponse({'error': 'User not authenticated'}, status=401)

@csrf_exempt
def check_authentication(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})
