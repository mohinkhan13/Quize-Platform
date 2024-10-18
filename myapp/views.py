from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseBadRequest

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
    try:
        user = CustomUser.objects.get(id=request.session['user_id'])        
        return render(request, 'index.html',{'user':user})
    except:
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
                        profile=request.FILES['profile']
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
                request.session['profile'] = user.profile.url
                exams_count = Exam.objects.filter(user=user).count()
                request.session['exams_count'] = exams_count
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
            del request.session['profile']
        except CustomUser.DoesNotExist:
            pass  # Handle the case if the user is not found    
    return redirect('login')  # Redirect to the login page
    
def setting(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'setting.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def profile(request):
    if request.method == 'POST':        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        country = request.POST['country']
        city = request.POST['city']
        address = request.POST['address']
        dob = request.POST['dob']
        profile = request.FILES.get('profile')
        print(profile)
        user = CustomUser.objects.get(id=request.session['user_id'])

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.mobile = mobile
        user.country = country
        user.city = city
        user.address = address
        user.dob = dob
        try:
            user.profile = profile
        except:
            pass
        user.save()
        request.session['profile'] = user.profile.url
        return redirect('profile')

    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'profile.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def change_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        try:
            user = CustomUser.objects.get(id=request.session['user_id'])

            context = {        
                'user':user,
            }
            return render(request, 'change_password.html', context)
        except:
            error = "You Need To login First"
            return render(request, 'login.html', {'error':error})
    
def forgot_password(request):
    if request.method == 'POST':
        # POST request handling logic
        pass
    else:
        # Check if user is logged in based on session
        user_id = request.session.get('user_id')
        if user_id:
            try:
                CustomUser.objects.get(id=user_id)  # Check if user exists
                logout(request)
                return redirect('forgot-password')  # If user exists, redirect to logout or a different page
            except CustomUser.DoesNotExist:
                pass  # If user doesn't exist, proceed to render the forgot password page

        return render(request, 'forgot_password.html')
    
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
            exam_name=request.POST['exam_name'],
            exam_subject=request.POST['exam_subject'],
            exam_type=request.POST['exam_type'],
            number_of_questions=int(request.POST['number_of_questions']),  # Convert to int
            time_setting=request.POST['time_setting'],
            exam_time=request.POST['exam_time'],
        )
        return redirect('create-questions', exam.id)  # Redirect to create questions view
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

            exam.question_created = True
            exam.save()
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
            exam.question_created = True
            exam.save()
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
            exam.question_created = True
            exam.save()
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
            exam.question_created = True
            exam.save()
            return redirect('create-questions', id=exam.id)
    else:
        number_of_questions = exam.number_of_questions
        mcqs = MCQQuestion.objects.filter(exam=exam)
        tf = TrueFalseQuestion.objects.filter(exam=exam)
        sa = ShortAnswerQuestion.objects.filter(exam=exam)

        all_questions = []
        
        # Add question_type attribute to each question
        for question in mcqs:
            question.question_type = 'MCQ'
            all_questions.append(question)
        
        for question in tf:
            question.question_type = 'TrueFalse'
            all_questions.append(question)

        for question in sa:
            question.question_type = 'ShortAnswer'
            all_questions.append(question)
         
        context = {
            'exam': exam,
            'number_of_questions': number_of_questions,
            'all_questions': all_questions,
        }
        return render(request, 'create_questions.html', context)
    
def publish_exam(request,id):
    try:
        exam = Exam.objects.get(id=id)

        exam.visibility = 'publish'
        exam.save()
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return redirect(referer_url)
        else:
            return redirect('my-all-exam')
    except Exam.DoesNotExist:
        return HttpResponseBadRequest("Exam not found.")


def private_exam(request,id):
    try:
        exam = Exam.objects.get(id=id)

        exam.visibility = 'private'
        exam.save()
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return redirect(referer_url)
        else:
            return redirect('my-all-exam') 
    except Exam.DoesNotExist:
        return HttpResponseBadRequest("Exam not found.")
    
def delete_exam(request, id):
    # Check if the request method is POST to confirm deletion
    exam = get_object_or_404(Exam, id=id)  # Retrieve the exam or return a 404 if not found
    exam.delete()  # Delete the exam
    return redirect('my-all-exams')  # Redirect to the exams list page (replace with your actual URL name)