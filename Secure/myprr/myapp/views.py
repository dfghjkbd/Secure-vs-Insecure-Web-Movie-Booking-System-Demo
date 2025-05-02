from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Movie, Booking
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection




from django.shortcuts import render, redirect
from .models import CustomUser

#from django.contrib.auth import authenticate, login
from .models import CustomUser
from .models import Feedback
from django.utils import timezone
from django.contrib import messages
from .models import Feedback

def feedback_page(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')  # latest first
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


def submit_feedback(request):
    if request.method == 'POST':
        feedback_msg = request.POST.get('feedback')
        username = request.session.get('username', 'Anonymous')
        escaped_username = username.replace("'", "''")

        if feedback_msg:
            Feedback.objects.create(
                username=escaped_username ,
                message=feedback_msg,
                submitted_at=timezone.now()
            )
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "Feedback cannot be empty.")

    return redirect('list_movies')  # Redirect to the movie listing page
def frontpage(request):
    return render(request, 'frontpage.html')

def signup_page(request):
    return render(request, 'signup.html')
def login_page(request):
    return render(request, 'login.html')
def welcome(request):
    return render(request, 'welcome.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username, password=password)  # Replace with proper password hashing in production
            request.session['username'] = user.username
            return redirect('list_movies')
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        age = request.POST['age']

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        CustomUser.objects.create(
            username=username,
            email=email,
            password=password,
            phone=phone,
            age=age
        )
        return redirect('login')
    return render(request, 'signup.html')

from .models import Movie

def list_movies(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_movie")
        movies = cursor.fetchall()

    return render(request, 'movies.html', {'movies': movies})

'''def list_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})'''
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

@csrf_protect
def book_movie(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return redirect('login')

        try:
            movie_id = int(request.POST.get('movie_id'))
            seats = int(request.POST.get('seats'))
        except (TypeError, ValueError):
            return HttpResponse("<h2>Invalid input. Booking failed.</h2>")

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return HttpResponse("<h2>Movie not found!</h2>")

        if seats <= movie.remaining_seats:
            movie.remaining_seats -= seats
            movie.save()

            Booking.objects.create(
                user=username,
                movie=movie.name,
                number_of_seats=seats,
                booking_time=datetime.now()
            )
            return redirect('list_movies')
        else:
            return HttpResponse(f"<h2>Only {movie.remaining_seats} seats left!</h2>")
    else:
        return redirect('list_movies')


'''def frontpage(request):
    return render(request, 'frontpage.html')

def signup_page(request):
    return render(request, 'signup.html')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        age = request.POST['age']

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        CustomUser.objects.create(
            username=username,
            email=email,
            password=password,
            phone=phone,
            age=age
        )
        return redirect('login')
    return render(request, 'signup.html')
        

def login_page(request):
    return render(request, 'login.html')

def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username, password=password)
            return render(request, 'welcome.html', {'user': user})
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
     

def welcome(request):
    return render(request, 'welcome.html')'''



