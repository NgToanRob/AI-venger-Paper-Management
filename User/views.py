
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
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token


@login_required(login_url="login")
def home(request):
    return render(request, "Authentication/home.html")


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # Get data from request body
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Check if a user with the given email already exists
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'message': 'User with this email already exists.'}, status=400)

        # Create a new user
        user = CustomUser.objects.create_user(name=name, email=email, password=password)

        if user:
            return JsonResponse({'message': 'User registered successfully.'})
        else:
            return JsonResponse({'message': 'Error occurred during registration.'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')) # Get data from request body
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me') == 'true'
        print(email, password, remember_me)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when the browser is closed
                
                return JsonResponse({'message': 'Login successful.'})
            else:
                return JsonResponse({'message': 'Your account is not active.'}, status=403)
        else:
            return JsonResponse({'message': 'Invalid email or password.'}, status=401)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def logout_view(request):
    logout(request)
    return redirect("login")

@csrf_exempt
@require_POST
def update_topics(request):
    user = request.user
    print(user)

    if user.is_authenticated:
        # User is logged in
        data = request.POST.getlist('topics')  # Assuming 'topics' is the name attribute in your form

        updated_topics = []

        for topic_name in data:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            user.topics.add(topic)
            updated_topics.append(topic.name)

        return JsonResponse({'message': 'Topics updated successfully', 'updated_topics': updated_topics}, status=200)
    else:
        # User is not logged in
        return JsonResponse({'error': 'User not authenticated'}, status=401)


    