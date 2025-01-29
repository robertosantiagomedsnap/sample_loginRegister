from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout


User = get_user_model()

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')

        if user_type == "personal":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            contact_number = request.POST.get('contact_number')
            employee_specialty = request.POST.get('employee_specialty')
            gender = request.POST.get('gender')

            if not first_name or not last_name or not contact_number:
                messages.error(request, "All personal fields are required.")
                return redirect('register')

            try:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    contact_number=contact_number,
                    employee_specialty=employee_specialty,
                    gender=gender,
                    user_type="personal",
                )
                messages.success(request, "Personal account registered successfully! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
                return redirect('register')

        elif user_type == "company":
            company_name = request.POST.get('company_name')
            num_employees = request.POST.get('num_employees')
            vat_number = request.POST.get('vat_number')
            company_phone = request.POST.get('company_phone')
            address = request.POST.get('address')
            country = request.POST.get('country')

            if not company_name or not num_employees or not vat_number or not company_phone or not address or not country:
                messages.error(request, "All company fields are required.")
                return redirect('register')

            try:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password1,
                    company_name=company_name,
                    num_employees=num_employees,
                    vat_number=vat_number,
                    company_phone=company_phone,
                    address=address,
                    country=country,
                    user_type="company",
                )
                messages.success(request, "Company account registered successfully! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
                return redirect('register')

    return render(request, 'accounts/register.html')




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # Ensure `authenticate` is correctly used

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


def home(request):
    user = request.user

    # Display company name if user is a company, otherwise first name
    display_name = user.company_name if user.user_type == "company" else user.first_name

    return render(request, 'accounts/home.html', {'display_name': display_name})



def user_logout(request):
    logout(request)

    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True  # This prevents old messages from showing again

    # Add only the logout success message
    messages.success(request, "You have been logged out successfully!")
    
    return redirect('login')  # Redirects to the login page

