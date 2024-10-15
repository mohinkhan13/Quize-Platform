from django.shortcuts import render

# Create your views here.
def index(request):
    # Your logic here
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            
        }
        return render(request, 'register.html', context)
    
def login(request):
    if request.method == 'POST':
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'login.html', context)
    
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

def create_exam(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        context = {
            # Add your context variables here
        }
        return render(request, 'create_exam.html', context)