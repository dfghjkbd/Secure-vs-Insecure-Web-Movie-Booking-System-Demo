from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.





from django.shortcuts import render, redirect
from .models import CustomUser
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from .models import Movie, Booking


from django.shortcuts import redirect
from django.contrib import messages
from .models import Feedback
from django.utils import timezone
from django.shortcuts import render
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
from django.db import connection
from django.http import HttpResponse

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        query = f"SELECT * FROM myapp_customuser WHERE username = '{username}' AND password = '{password}'"

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchone()
        except Exception as e:
            return HttpResponse(f"<h2>SQL Error: {e}</h2>")

        if user:
            request.session['username'] = username
            return redirect('list_movies')
            #return render(request, 'welcome.html', {'user': user})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


'''def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # ❌ VULNERABLE SQL query directly using user input
        query = f"SELECT * FROM app_customuser WHERE username = '{username}' AND password = '{password}'"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return render(request, 'welcome.html', {'user': user})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')'''

'''def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username, password=password)
            return render(request, 'welcome.html', {'user': user})
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')'''
     

def welcome(request):
    return render(request, 'welcome.html')


def list_movies(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_movie")
        movies = cursor.fetchall()

    return render(request, 'movies.html', {'movies': movies})

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection

@csrf_exempt  # Insecure setup for demonstration purposes
def book_movie(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return redirect('login')

        try:
            movie_id = int(request.POST.get('movie_id', ''))
            seats = int(request.POST.get('seats', ''))
        except (ValueError, TypeError):
            return HttpResponse("<h2>Invalid input. Booking failed.</h2>")

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM myapp_movie WHERE id = {movie_id}")
                movie = cursor.fetchone()

            if movie:
                movie_name = movie[1]
                remaining = movie[4]

                if seats <= remaining:
                    new_remaining = remaining - seats

                    try:
                        # Escape single quotes in username and movie_name for SQL
                        escaped_username = username.replace("'", "''")
                        escaped_movie_name = movie_name.replace("'", "''")

                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                                INSERT INTO myapp_booking (user, movie, number_of_seats, booking_time)
                                VALUES ('{escaped_username}', '{escaped_movie_name}', {seats}, datetime('now'))
                            """)
                            cursor.execute(f"""
                                UPDATE myapp_movie SET remaining_seats = {new_remaining} WHERE id = {movie_id}
                            """)
                        return redirect('list_movies')
                    except Exception as e:
                        return HttpResponse(f"<h2>Booking Error: {e}</h2>")
                else:
                    return HttpResponse(f"<h2>Only {remaining} seats left!</h2>")
            else:
                return HttpResponse("<h2>Movie not found!</h2>")
        except Exception as e:
            return HttpResponse(f"<h2>Error fetching movie: {e}</h2>")
    else:
        return redirect('list_movies')


'''@csrf_exempt  # Insecure setup for demonstration purposes
def book_movie(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return redirect('login')

        try:
            movie_id = int(request.POST.get('movie_id', ''))
            seats = int(request.POST.get('seats', ''))
        except (ValueError, TypeError):
            return HttpResponse("<h2>Invalid input. Booking failed.</h2>")

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM myapp_movie WHERE id = {movie_id}")
                movie = cursor.fetchone()

            if movie:
                movie_name = movie[1]
                remaining = movie[4]

                if seats <= remaining:
                    new_remaining = remaining - seats

                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                                INSERT INTO myapp_booking (user, movie, number_of_seats, booking_time)
                                VALUES ('{username}', '{movie_name}', {seats}, datetime('now'))
                            """)
                            cursor.execute(f"""
                                UPDATE myapp_movie SET remaining_seats = {new_remaining} WHERE id = {movie_id}
                            """)
                        return redirect('list_movies')
                    except Exception as e:
                        return HttpResponse(f"<h2>Booking Error: {e}</h2>")
                else:
                    return HttpResponse(f"<h2>Only {remaining} seats left!</h2>")
            else:
                return HttpResponse("<h2>Movie not found!</h2>")
        except Exception as e:
            return HttpResponse(f"<h2>Error fetching movie: {e}</h2>")
    else:
        return redirect('list_movies')'''


''''from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 👈 Required only if you haven't added {% csrf_token %} in form
def book_movie(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return redirect('login')

        movie_id = request.POST['movie_id']
        seats = int(request.POST['seats'])

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM myapp_movie WHERE id = {movie_id}")
            movie = cursor.fetchone()

        if movie:
            movie_name = movie[1]
            remaining = movie[4]

            if seats <= remaining:
                new_remaining = remaining - seats
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"""
                            INSERT INTO myapp_booking (user, movie, number_of_seats, booking_time)
                            VALUES ('{username}', '{movie_name}', {seats}, datetime('now'))
                        """)
                        cursor.execute(f"""
                            UPDATE myapp_movie SET remaining_seats = {new_remaining} WHERE id = {movie_id}
                        """)
                    return redirect('list_movies')  # 👈 Redirect after booking
                except Exception as e:
                    return HttpResponse(f"<h2>Booking Error: {e}</h2>")
            else:
                return HttpResponse(f"<h2>Only {remaining} seats left!</h2>")
        else:
            return HttpResponse("<h2>Movie not found!</h2>")
    else:
        return redirect('list_movies')'''




