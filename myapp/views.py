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
    try:
        user = CustomUser.objects.get(id=request.session['user_id'])
        exams = Exam.objects.filter(user=user)
        context = {
            'exams':exams,
        }
        return render(request, 'my_all_exams.html', context)
    except:
        exams = None
        context = {
            'exams':exams,
        }
        return render(request, 'my_all_exams.html', context)

@login_required
def create_exam(request):
    if request.method == 'POST':
        print(request.POST)
        user_id = request.session.get('user_id')
        user = CustomUser.objects.get(id=user_id)

        exam = Exam.objects.create(
            user=user,
            exam_name = request.POST['exam_name'],
            exam_subject = request.POST['exam_subject'],
            exam_type = request.POST['exam_type'],
            number_of_questions = request.POST['number_of_questions'],
            time_setting = request.POST['time_setting'],
            exam_time = request.POST['exam_time'],
        )
        return render(request, 'create_questions.html',{'exam':exam} )
    return render(request, 'create_exam.html')
    
def create_questions(request,id):
    exam = Exam.objects.get(id=id)
    if request.method == 'POST':
        print("Request POST Data:", request.POST)
        
        # Determine exam type
        exam_type = exam.exam_type  # Ensure your form has this input
        print(f"Exam type {exam_type}")
        if exam_type == 'MX':
            # For mixed type, capture the counts
            mcq_count = int(request.POST.get('mcq_count', 0))  # Count of MCQs
            tf_count = int(request.POST.get('tf_count', 0))    # Count of True/False questions
            
            mcq_questions = []
            tf_questions = []
            
            # Process MCQ Questions
            for i in range(1, mcq_count + 1):
                question = request.POST.get(f'question_{i}','').strip()
                option_a = request.POST.get(f'option_a_{i}','').strip()
                option_b = request.POST.get(f'option_b_{i}','').strip()
                option_c = request.POST.get(f'option_c_{i}','').strip()
                option_d = request.POST.get(f'option_d_{i}','').strip()
                correct_answer = request.POST.get(f'correct_answer_{i}','').strip()
                
                if question:  # Ensure there's a question
                    mcq_questions.append({
                        'question': question,
                        'options': {
                            'A': option_a,
                            'B': option_b,
                            'C': option_c,
                            'D': option_d
                        },
                        'correct_answer': correct_answer
                    })

                    # Save to the database
                    MCQQuestion.objects.create(
                        exam=exam,
                        question=question,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )

            # Process True/False Questions
            for i in range(1, tf_count + 1):
                question = request.POST.get(f'tf-question_{i}','').strip()  # Adjust as necessary
                correct_answer = request.POST.get(f'tf-correct-answer_{i}','').strip()
                
                if question:  # Check to ensure we have a question
                    tf_questions.append({
                        'question': question,
                        'correct_answer': correct_answer
                    })

                    # Save to the database
                    TrueFalseQuestion.objects.create(
                        exam=exam,
                        question=question,
                        correct_answer=(correct_answer == 'True')  # Convert to boolean
                    )

            # Debugging Output
            print("MCQ Questions:", mcq_questions)
            print("True/False Questions:", tf_questions)

            # After saving, you can redirect or return a response
            return redirect('create-questions', id=exam.id)
        
        elif exam_type == 'MCQ':
            # Handle MCQ-specific logic
            mcq_count = exam.number_of_questions # Count of MCQs
            
            for i in range(1, mcq_count + 1):
                question = request.POST.get(f'question_{i}','').strip()
                option_a = request.POST.get(f'option_a_{i}','').strip()
                option_b = request.POST.get(f'option_b_{i}','').strip()
                option_c = request.POST.get(f'option_c_{i}','').strip()
                option_d = request.POST.get(f'option_d_{i}','').strip()
                correct_answer = request.POST.get(f'correct_answer_{i}','').strip()
                
                if question:  # Ensure there's a question
                    # Save to the database
                    MCQQuestion.objects.create(
                        exam=exam,
                        question=question,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        correct_answer=correct_answer,
                    )

            return redirect('create-questions', id=exam.id)
        
        elif exam_type == 'TF':
            # Handle True/False specific logic
            tf_count = exam.number_of_questions  # Count of True/False questions
            
            for i in range(1, tf_count + 1):
                question = request.POST.get(f'tf-question_{i}', '').strip()  # Get the full question text
                correct_answer = request.POST.get(f'tf-correct-answer_{i}', '').strip()
                
                if question:  # Check to ensure we have a question
                    # Save to the database
                    TrueFalseQuestion.objects.create(
                        exam=exam,
                        question=question.strip(),  # Ensure leading/trailing whitespace is removed
                        correct_answer=(correct_answer == 'True')  # Convert to boolean
                    )

            return redirect('create-questions', id=exam.id)


        
        elif exam_type == 'SA':
            # Handle Short Answer logic
            sa_count = exam.number_of_questions  # Count of Short Answer questions
            
            for i in range(1, sa_count + 1):
                question = request.POST.get(f'sa-question_{i}', '').strip()
                correct_answer = request.POST.get(f'sa-correct-answer_{i}', '').strip()
                
                if question:  # Ensure there's a question
                    # Save to the database
                    ShortAnswerQuestion.objects.create(
                        exam=exam,
                        question=question,
                        correct_answer=correct_answer,
                    )

            return redirect('create-questions', id=exam.id)
    else:
        
        number_of_questions = exam.number_of_questions 
        context = {
           'exam':exam,
           'number_of_questions': number_of_questions,
        }
        return render(request, 'create_questions.html', context)