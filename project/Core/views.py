from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_protect
# Create your views here.


# views.py
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, date
from .models import LoginStreak



# *******************************************************************

def firstpage(request):
    return render(request,'firstpage.html')

@login_required
def Home(request):
    today = timezone.now().date()

    # Get or create today's login streak for the user
    streak, created = LoginStreak.objects.get_or_create(user=request.user, date=today)

    # Get the last 4 weeks of login data, excluding Sundays
    start_date = today - timedelta(days=27)  # Approximately 4 weeks back
    streak_data = LoginStreak.objects.filter(
        user=request.user,
        date__gte=start_date
    ).exclude(date__week_day=1)  # Exclude Sundays (if that's the requirement)

    # Organize streak data by weeks (Monday-Saturday)
    weekly_data = {}
    for i in range(4):
        week_start = today - timedelta(days=(i * 7 + today.weekday()))  # Calculate Monday of each week
        weekly_data[f"Week {4 - i}"] = [
            streak_data.filter(date=week_start + timedelta(days=day)).first()  # Get login data for each day
            for day in range(6)  # Only for Monday-Saturday
        ]
    
    # Pass the current week and last 4 weeks' data to the template
    return render(request, 'index.html', {
        'current_week': weekly_data["Week 4"],  # Show only the current week by default
        'last_4_weeks': weekly_data,  # Include all weeks for expanding view
        'created': created,  # Whether today's login entry is new
    })


def RegisterView(request):
    if request.method=="POST":
        first_name= request.POST.get('first_name')
        second_name=request.POST.get('second_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_data_has_error=False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')
        
        if len(password)<5:
            user_data_has_error=True
            messages.error(request, 'Password must be atleast of 5 characters')

        if user_data_has_error==False:
            new_user= User.objects.create_user(
                first_name=first_name,
                last_name=second_name,
                email=email,
                username=username,
                password=password
            )
            messages.success(request,'Account created, Login now')
            return redirect('login')
        else:
            return redirect('register')


    return render(request, 'register.html')

@csrf_protect
def LoginView(request):
    if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')

            # authenticate the user detail
            user= authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid login credentials')
                return redirect('login')
            
    return render(request, 'login.html')


def LogoutView(request):
    logout(request)
    return redirect('firstpage')


def ForgotPassword(request):
    if request.method=="POST":
        email=request.POST.get('email')

        try:
            user=User.objects.get(email=email)

             # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # creat password reset ur;
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url= f'{request.scheme}://{request.get_host()}{password_reset_url}'
            # email content
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER, 
                [email] 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)


        except User.DoesNotExist:
            messages.error(request, f"No user with email {email} found")
            return redirect('forgot-password')


    return render(request, 'forgot_password.html')


def PasswordResetSent(request, reset_id):
        if PasswordReset.objects.filter(reset_id=reset_id).exists():
            return render(request, 'password_reset_sent.html')
        else:
            # redirect to forgot password page if code does not exist
            messages.error(request, 'Invalid reset id')
            return redirect('forgot-password')

def ResetPassword(request, reset_id):
    try:
        reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            # check to make sure link has not expired
            expiration_time = reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                reset_id.delete()
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
            
            if not passwords_have_error:
                user = reset_id.user
                user.set_password(password)
                user.save()
                
                # delete reset id after use
                reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')

            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')




#  ****************************************************************************************

# views.py
# from django.shortcuts import render
# from django.utils import timezone
# from datetime import timedelta
# from .models import LoginStreak
# from django.contrib.auth.decorators import login_required

@login_required
def daily_login(request):
    today = timezone.now().date()

    # Get or create today's login streak for the user
    streak, created = LoginStreak.objects.get_or_create(user=request.user, date=today)

    # Get the last 4 weeks of login data, excluding Sundays
    start_date = today - timedelta(days=27)  # Approximately 4 weeks back
    streak_data = LoginStreak.objects.filter(
        user=request.user,
        date__gte=start_date
    ).exclude(date__week_day=1)  # Exclude Sundays (if that's the requirement)

    # Organize streak data by weeks (Monday-Saturday)
    weekly_data = {}
    for i in range(4):
        week_start = today - timedelta(days=(i * 7 + today.weekday()))  # Calculate Monday of each week
        weekly_data[f"Week {4 - i}"] = [
            streak_data.filter(date=week_start + timedelta(days=day)).first()  # Get login data for each day
            for day in range(6)  # Only for Monday-Saturday
        ]

    # Pass the data to the template
    return render(request, 'streak.html', {
        'current_week': weekly_data["Week 4"],  # Show only the current week by default
        'last_4_weeks': weekly_data,  # Include all weeks for expanding view
        'created': created,  # Whether today's login entry is new
    })



def streak_view(request):
    # Sample data for the current week and last 4 weeks
    current_week = [
        {'date': '2024-11-10', 'login': True},  # Example data
        {'date': '2024-11-11', 'login': False},
        {'date': '2024-11-12', 'login': True},
        {'date': '2024-11-13', 'login': False},
        {'date': '2024-11-14', 'login': True},
        {'date': '2024-11-15', 'login': True},
        {'date': '2024-11-16', 'login': False},
    ]

    # Last 4 weeks' data structure
    last_4_weeks = {
        'Week 1': [{'date': '2024-10-13', 'login': True}, {'date': '2024-10-14', 'login': False}, {'date': '2024-10-15', 'login': True}],
        'Week 2': [{'date': '2024-10-20', 'login': False}, {'date': '2024-10-21', 'login': True}],
        'Week 3': [{'date': '2024-10-27', 'login': True}, {'date': '2024-10-28', 'login': True}],
        'Week 4': [{'date': '2024-11-03', 'login': False}, {'date': '2024-11-04', 'login': True}],
    }

    context = {
        'current_week': current_week,
        'last_4_weeks': last_4_weeks
    }
    return render(request, 'streak.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookIssue
from django.contrib import messages


from django.contrib.auth.decorators import user_passes_test



# Check if the user is an admin
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import User, Book, BookIssue

@admin_required
def issue_book(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        book_id = request.POST.get("book_id")

        # Fetch user and book instances using get_object_or_404 for better error handling
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, id=book_id)

        # Check if the book is available
        if book.available_copies > 0:
            issued_count = BookIssue.objects.filter(user=user, returned=False).count()

            # Check if the user has already issued 5 books
            if issued_count >= 5:
                messages.error(request, f"{user.username} already has 5 books issued.")
            else:
                # Issue the book
                due_date = timezone.now() + timedelta(days=28)
                BookIssue.objects.create(
                    user=user,
                    book=book,
                    issue_date=timezone.now(),
                    due_date=due_date,
                )
                book.available_copies -= 1
                book.save()
                messages.success(request, f"{book.title} issued to {user.username}.")
        else:
            messages.error(request, f"{book.title} is currently unavailable.")

    users = User.objects.all()
    books = Book.objects.all()
    return render(request, 'issue_book.html', {'users': users, 'books': books})

@login_required
def return_book(request, issue_id):
    # Get the issued book record using get_object_or_404 to raise a 404 if not found
    issued_book = get_object_or_404(BookIssue, id=issue_id, user=request.user, returned=False)

    # Mark the book as returned and handle fine calculation
    overdue_days = (timezone.now().date() - issued_book.due_date).days
    if overdue_days > 0:
        issued_book.fine = overdue_days * 2  # Assuming fine rate of 2 per day
    issued_book.returned = True
    issued_book.save()

    # Update the book's available copies
    issued_book.book.available_copies += 1
    issued_book.book.save()

    messages.success(request, f"The book '{issued_book.book.title}' has been returned successfully.")
    return redirect('user_issued_books')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def issued_books(request):
    issued_books = BookIssue.objects.filter(user=request.user, returned=False)
    return render(request, 'issued_books.html', {'issued_books': issued_books})

@login_required
def user_issued_books(request):
    issued_books = BookIssue.objects.filter(user=request.user, returned=False)
    return render(request, 'user_issued_books.html', {'issued_books': issued_books})

