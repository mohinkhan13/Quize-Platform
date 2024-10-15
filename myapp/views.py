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