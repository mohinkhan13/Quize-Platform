from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password

def login_required(view_func, login_url='login.html', message=None):
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')  
        if not user_id or not CustomUser.objects.filter(id=user_id, is_login=True).exists():
            return render(request, login_url, {
                'error': "You must be logged in to Access All Pages.",
                'next': request.path
            })
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

# Create your views here.
def index(request):
    # Your logic here
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the email or username already exists
        try:
            user = CustomUser.objects.get(email=email)
            error = "Email already exists"
            return render(request, 'register.html', {'error': error})
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(username=username)
                error = "Username already exists"
                return render(request, 'register.html', {'error': error})
            except CustomUser.DoesNotExist:
                # If both email and username do not exist, continue with registration
                if password == confirm_password:
                    hashed_password = make_password(password)
                    
                    # Create the new user
                    CustomUser.objects.create(
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        username=username,
                        email=email,
                        mobile=request.POST['mobile'],
                        password=hashed_password,
                    )
                    msg = "Registration Successful! Please login."
                    return render(request, 'login.html', {'msg': msg})
                else:
                    error = "Password and confirm password do not match"
                    return render(request, 'register.html', {'error': error})

    return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)

            if check_password(password, user.password):
                user.is_login = True
                user.save()
                request.session['user_id'] = user.id 
                return render(request, 'index.html')
            else:
                error = "Invalid Password"
                return render(request, 'login.html', {'error' : error} )
        except CustomUser.DoesNotExist:
            error = "Email not registered"
            return render(request, 'login.html', {'error' :error } )
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'login.html', context)

def logout(request):

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = CustomUser.objects.get(id=user_id)
            # Set the is_login attribute to False if you are using it
            user.is_login = False            
            user.save()  # Save the user status if needed
            del request.session['user_id']
        except CustomUser.DoesNotExist:
            pass  # Handle the case if the user is not found    
    return redirect('login')  # Redirect to the login page
    
def setting(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'setting.html', context)
    
def profile(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'profile.html', context)
    
def change_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'change_password.html', context)
    
def forgot_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'forgot_password.html', context)
    
def verify_otp(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'verify_otp.html', context)

def new_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'new_password.html', context)
    
def my_all_exams(request):
    # Your logic here
    context = {}
    return render(request, 'my_all_exams.html', context)

@login_required
def create_exam(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'create_exam.html', context)
    
def create_questions(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'create_questions.html', context)