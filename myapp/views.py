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