from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import CustomUser
from accounts.models import CustomUser  # Import your CustomUser model
from django.shortcuts import render, redirect

User = get_user_model()

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        contact_number = request.POST.get('contact_number')
        employee_type = request.POST.get('employee_type')
        gender = request.POST.get('gender')

        # Validate first name
        if not first_name:
            messages.error(request, "First name is required.")
            return redirect('register')

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check for existing email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                contact_number=contact_number,
                employee_type=employee_type,
                gender=gender,
            )
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {e}")
            return redirect('register')

    return render(request, 'accounts/register.html')



def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # 'username' here maps to 'email' because of USERNAME_FIELD
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')  # Replace with your login template path


def home(request):
    user = request.user
    return render(request, 'accounts/home.html', {'name': user.first_name})



def user_logout(request):
    logout(request)
    # Clear all messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')  # Replace 'login' with your login URL name
