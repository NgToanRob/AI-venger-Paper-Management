
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request):
    return render(request, "Authentication/home.html")


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        accept_terms = request.POST.get('accept_terms') == 'true'

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Check if user accepted terms
        if not accept_terms:
            return JsonResponse({'error': 'You must accept the terms'}, status=400)

        # Create a new user
        User = get_user_model()
        try:
            user = User.objects.create_user(
                email=email, name=name, password=password)
            return JsonResponse({'message': 'Registration successful'})
        except IntegrityError:
            return JsonResponse({'error': 'User with this email already exists'}, status=400)

    # Return error for unsupported request methods (GET, etc.)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def login_view(request):
    if request.method == 'POST':
        # Get the email and password from the request data
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get(
            'remember_me') == 'true'  # Convert to boolean

        # Implement your login logic here
        # For example, you can use Django's built-in authentication system:
        from django.contrib.auth import authenticate, login

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Successful login
            login(request, user)

            # Return success response
            return JsonResponse({'message': 'Login successful'})
        else:
            # Failed login
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # Return error for unsupported request methods (GET, etc.)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
@require_POST
def update_domains(request):
    user = request.user
    domains = request.POST.get('domains', '')
    
    user.domains = domains
    user.save()

    return JsonResponse({'message': 'Domains updated successfully'})