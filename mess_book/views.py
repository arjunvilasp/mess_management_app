
from django.shortcuts import redirect, render
from mess_book.models import Student, Attendance, Bill, Complaint, Admin, Meal, LeaveRequest, Feedback, Booking
from datetime import date, datetime, timedelta
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .decorator import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
import json
import uuid
from django.db.models import Sum
# Create your views here.


# Home page
def home(request):
    return render(request,'home.html')





# Login
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Check if the user is an admin
            try:
                admin = Admin.objects.get(username=username)
                # if check_password(password, admin.password):
                if password == admin.password:
                    request.session['admin_id'] = admin.id
                    return redirect('dashboard')
                else:
                    error_message = "Invalid username or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except Admin.DoesNotExist:
                pass  

            # Check if the user is a student
            try:
                student = Student.objects.get(username=username)
                if check_password(password, student.password):
                    request.session['student_id'] = student.id
                    request.session['studentId'] = student.student_id
                    request.session['name'] = student.username
                    return redirect('studhome')
                else:
                    error_message = "Invalid username or password."
                    return render(request, 'login.html', {'error_message': error_message})
            except Student.DoesNotExist:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Username and password are required."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')





# Register
def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        student_id = request.POST.get('student_id')
        room_no = request.POST.get('room_no')
        email = request.POST.get('email')
        password = request.POST.get('password')

        hashed_password = make_password(password)

        student = Student(username=username.capitalize(), student_id=student_id,room_no = room_no ,email=email, password=hashed_password)
        student.save()

        messages.success(request, 'Student Registration Success.')
        return redirect('/login/')
    else:
        return render(request, 'register.html')

def Logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']  
    return redirect('login') 





# Profile
@login_required
def profile(request, user_id):
    
    student = get_object_or_404(Student, pk=user_id)

    student_data = {
        'username': student.username,
        'email': student.email,
        'student_id':student.student_id,
        'room_no':student.room_no
    }
    return render(request, 'profile.html', {'student': student_data})





@login_required
def update_profile(request, user_id):

    user = get_object_or_404(Student, pk=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.student_id = request.POST.get('student_id')
        user.room_no = request.POST.get('room_no')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        request.session['studentId'] = request.POST.get('student_id')
        request.session['name'] = request.POST.get('username')
        request.session.save()
        return redirect('profile', user_id=user.id)
    return render(request, 'profile.html', {'user': user})



@login_required
def update_password(request, user_id):

    user = get_object_or_404(Student, pk=user_id)

    if request.method == 'POST':
        current_pasword = request.POST.get('current_pass')
        new_password = request.POST.get('new_pass')
        print(current_pasword,new_password)
        if(check_password(current_pasword,user.password)):
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('profile', user_id=user.id)
        else:
            messages.error(request, 'Current Password Mismatched..!')
            return redirect('profile', user_id=user.id)
        
    return render(request, 'update_profile.html', {'user': user})





# Student hom
@login_required
def studhome(request):
    count = LeaveRequest.objects.filter(status__in=[1, 2],seen=0).count()
    return render(request,'studhome.html',{'notifications_count' : count })




@login_required
def more(request):
    return render(request,'more.html')




# Notification
@login_required
def notifications(request, student_id):

    notifications = LeaveRequest.objects.filter(student_id=student_id, status__in=[1, 2], seen=0)

    for notification in notifications:
        notification.seen = 1
        notification.save()

    return render(request, 'notifications.html', {'notifications': notifications})



@login_required
def mark_as_seen(request, notification_id):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        notification = get_object_or_404(LeaveRequest, pk=notification_id, student_id=student_id)
        notification.seen = 1  
        notification.save()
    return redirect('notifications')




#Feedback
@login_required
def submit_feedback(request, student_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        print(rating_value)
        try:
            student = Student.objects.get(id=student_id)
            existing_feedback = Feedback.objects.filter(student=student).first()

            if existing_feedback:
                existing_feedback.rating = rating_value
                existing_feedback.save()
                messages.success(request, 'Feedback updated successfully')
            else:
                feedback = Feedback.objects.create(student=student, rating=rating_value)
                messages.success(request, 'Feedback submitted successfully')

        except Student.DoesNotExist:
            messages.error(request, 'Student does not exist')

        return redirect('studhome')
    else:
        return HttpResponse('Method not allowed', status=405)



@login_required
def mess(request):
    weekdays_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    weekly_meals = {day: {'breakfast': '', 'lunch': '', 'tea': '', 'dinner': ''} for day in weekdays_order}

    meals = Meal.objects.all()

    for meal in meals:
        weekly_meals[meal.day][meal.type.lower()] = meal.name  

    return render(request, 'mess.html', {'weekly_meals': weekly_meals})



    
from decimal import Decimal

from django.db.models import Q


@login_required
def book_meal(request, student_id):
    if request.method == 'POST':
        # Get selected meal types from the POST data
        selected_meals = request.POST.getlist('selected_meals')

        if not selected_meals:
            return JsonResponse({'error': 'No meals selected.'}, status=400)

        # Get today's date
        today_date = date.today()
        # Calculate tomorrow's date and set the time to 00:00:00
        tomorrow_date = timezone.now() + timedelta(days=1)
        tomorrow_date = tomorrow_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Check if the user has already booked for today
        existing_booking = Booking.objects.filter(
            Q(student_id=student_id) & 
            Q(date=tomorrow_date) 
        ).exists()

        if existing_booking:
            messages.success(request, 'User has already booked meal(s).')
            return redirect('studhome')

        # Calculate total price of selected meals
        weekday_name = today_date.strftime('%A')
        total_price = Meal.objects.filter(day=weekday_name, type__in=selected_meals).aggregate(total=Sum('price'))['total'] or Decimal('0.00')

        # Get the user object based on the user ID
        student = get_object_or_404(Student, id=student_id)

        # Update the bill for the user or create a new one if it doesn't exist
        current_month = timezone.now().strftime('%B')
        bill, created = Bill.objects.get_or_create(student=student, month=current_month, defaults={'amount': total_price})
        if not created:
            bill.amount += total_price
            bill.save()

        meal_types_str = ','.join(selected_meals)  # Convert the list to a comma-separated string

        # Create a booking with the meal types
        booking = Booking.objects.create(
            student=student,
            meal_types=meal_types_str,
            date=tomorrow_date,
            stud_id=student.student_id
        )
        messages.success(request, 'Meal(s) booked successfully!')
        return redirect('studhome')
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    


@login_required
def user_booking(request, user_id):
    user = get_object_or_404(Student, id=user_id)
    
    # Get today's date and tomorrow's date
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Filter bookings for today or tomorrow
    bookings = Booking.objects.filter(student=user, date__in=[today, tomorrow])

    for booking in bookings:
        # Convert the comma-separated string to a list
        booking.meal_types = booking.meal_types.split(',') if booking.meal_types else []

    context = {
        'bookings': bookings,
    }
    return render(request, 'user_booking.html', context)




@login_required
def user_complaints(request, student_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            try:
                student = Student.objects.get(pk=student_id)
                complaint = Complaint(student=student, message=message)
                complaint.save()
                messages.success(request, 'Complaint submitted successfully.')
            except Student.DoesNotExist:
                messages.error(request, 'Error: Student does not exist.')
        else:
            messages.error(request, 'Error: Empty message.')

        # Redirect to the 'complaints' URL with the student_id as a parameter
        return redirect(reverse('complaints', kwargs={'student_id': student_id})) 
    return render(request, 'complaints.html')


@login_required
def bill(request):
    return render(request,'user_bill.html')


@login_required
def view_bill(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_data = {
        'id':student.id,
        'username': student.username,
        'student_id': student.student_id,
        'email': student.email,
        # Add other fields you want to include
    }
    student_bills = Bill.objects.filter(student_id=student_id)
    context = {
        'student': student_data,
        'student_bills': student_bills,
    }
    return render(request, 'user_bill.html', context)


@login_required
def leave_req(request):
    return render(request,'leave_req.html')

@login_required
def attendance(request):
    return render(request,'attendance.html')


@login_required
def get_attendance_data(request, student_id):
    # Get the student object
    student = Student.objects.get(id=student_id)

    print(student_id)

    # Fetch the attendance data for the student
    attendance_data = Attendance.objects.filter(student=student).values('date', 'present')

    # Convert the queryset to a list of dictionaries
    attendance_list = list(attendance_data)

    # Prepare the data for FullCalendar
    events = []
    today = timezone.now().date()
    for record in attendance_list:
        event = {
            'title': 'Present' if record['present'] else 'Absent',
            'start': record['date'].strftime('%Y-%m-%d'),
            'backgroundColor': 'green' if record['present'] else 'red',
            'borderColor': 'green' if record['present'] else 'red',
            'classNames': ['present' if record['present'] else 'absent']
        }
        events.append(event)

    # Add unmarked days
    start_date = attendance_list[0]['date'] if attendance_list else today
    end_date = attendance_list[-1]['date'] if attendance_list else today

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        if not any(event['start'] == date_str for event in events):
            event = {
                'start': date_str,
                'backgroundColor': 'grey',
                'borderColor': 'grey',
                'classNames': ['unmarked']
            }
            events.append(event)
        current_date += timezone.timedelta(days=1)

    return JsonResponse(events, safe=False)

@login_required
def leave_request(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        reason = request.POST.get('reason')

        # Assuming you have a way to get the student object based on the student_id
        student = Student.objects.get(id=student_id)

        # Create the leave request object
        leave_request = LeaveRequest(student=student, date=date, reason=reason)
        leave_request.save()

        messages.success(request, 'Leave request submitted successfully.')
        return redirect('studhome')  # Redirect to student dashboard or any other page
    else:
        # Handle GET request or render the form
        return render(request, 'leave_req.html')

@login_required
def meal_list(request):
    meals = Meal.objects.all()
    return render(request, 'mess.html', {'meals': meals})


#admin views
@login_required
def dashboard(request):
    return render(request,'admin_dashboard/dashboard.html')

@login_required
def user_list(request):
    users = Student.objects.all()
    return render(request, 'admin_dashboard/users.html', {'users': users})
 
    
@login_required
def meal(request):
    return render(request,'admin_dashboard/meal.html')

@login_required
def get_meals(request):
    meals = Meal.objects.all()
    meal_data = [{'id': meal.id, 'name': meal.name, 'type': meal.type, 'day': meal.day, 'price': meal.price} for meal in meals]
    return JsonResponse(meal_data, safe=False)


@login_required
@csrf_exempt
def update_meal(request, meal_id):
    if request.method == 'PUT':
        try:
            meal = Meal.objects.get(id=meal_id)
            data = json.loads(request.body)
            meal.name = data.get('name', meal.name)
            meal.type = data.get('type', meal.type)
            meal.day = data.get('day', meal.day)
            meal.price = data.get('price', meal.price)
            meal.save()
            return JsonResponse({'message': 'Meal updated successfully!'})
        except Meal.DoesNotExist:
            return JsonResponse({'error': 'Meal not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    

@login_required
def add_meal(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        day = request.POST.get('day')
        price = request.POST.get('price')

        # Check if any required field is empty
        if not name or not type or not day or not price:
            return render(request, 'admin_dashboard/addMeal.html', {'error': 'All fields are required.'})

        try:
            # Create and save the Meal object
            meal = Meal(name=name, type=type, day=day, price=price)
            meal.save()
            # Redirect to a success page or another appropriate page
            return render(request, 'admin_dashboard/addMeal.html', {'message': 'Meal added succsessfully.'})
        except IntegrityError:
            # Handle duplicate entry error
            return render(request, 'admin_dashboard/addMeal.html', {'error': 'Duplicate entry. Meal with this day and type already exists.'})

    # Render the add meal form page for GET requests
    return render(request, 'admin_dashboard/addMeal.html')



@login_required
def delete_user(request, user_id):
    user = Student.objects.get(pk=user_id)
    if user:
        user.delete()
    return redirect('users_list')




@login_required
def mark_attendance(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        attendance_status = request.POST.get('attendance_status')

        student = Student.objects.get(id=user_id)

        today_date = date.today()

        attendance_record = Attendance.objects.filter(student=student, date=today_date).first()

        if attendance_record:
            attendance_record.present = (attendance_status == 'present')
            attendance_record.save()
        else:
            attendance = Attendance.objects.create(student=student, date=today_date, present=(attendance_status == 'present'))
            attendance.save()

        return JsonResponse({'success': True})
    else:
        students = Student.objects.all()
        return render(request, 'admin_dashboard/stud_attendance.html', {'students': students})



@login_required
def complaints(request):

    complaints = Complaint.objects.select_related('student').all()
    
    for complaint in complaints:
        complaint.seen = 1
        complaint.save()
    context = {
        'complaints': complaints,
    }
    return render(request, 'admin_dashboard/complaints.html', context)


@login_required
def delete_complaint(request, complaint_id):
    complaint = Complaint.objects.get(pk=complaint_id)
    if complaint:
        complaint.delete()
    return redirect('complaints')

@login_required
def leave_requests(request):

    leave_requests = LeaveRequest.objects.select_related('student').filter(status=0)
    leave_requests_history = LeaveRequest.objects.select_related('student')
    
    context = {
        'leave_requests': leave_requests,
        'leave_requests_history':leave_requests_history
    }

    for leave_request in leave_requests_history:
        leave_request.admin_seen = 1
        leave_request.save()
    return render(request, 'admin_dashboard/leaveRequests.html', context)


def allow_leave(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, pk=request_id)
    leave_request.status = 1  
    leave_request.save()
    return redirect('leave_requests')



def disallow_leave(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, pk=request_id)
    leave_request.status = 2  
    leave_request.save()
    return redirect('leave_requests')


@login_required
def display_ratings(request):
    ratings = Feedback.objects.all()

    context = {
        'ratings': ratings,
    }
    return render(request, 'admin_dashboard/ratings.html', context)




@login_required
def booking_count(request):
    if request.method == 'POST':
        date = request.POST.get('date');
        print(date)
        breakfast_count = Booking.objects.filter(meal_types__contains='breakfast',date=date).count()
        lunch_count = Booking.objects.filter(meal_types__contains='lunch',date=date).count()
        tea_count = Booking.objects.filter(meal_types__contains='tea',date=date).count()
        dinner_count = Booking.objects.filter(meal_types__contains='dinner',date=date).count()

        context = {
            'response':True,
            'breakfast_count': breakfast_count,
            'lunch_count': lunch_count,
            'tea_count': tea_count,
            'dinner_count': dinner_count,
        }
        return render(request,'admin_dashboard/booking_count.html',context)
    return render(request,'admin_dashboard/booking_count.html')


def view_stud_attendance(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'admin_dashboard/view_stud_attendance.html', context)



@login_required
def view_attendance_data(request, student_id):
    # Get the student object
    student = Student.objects.get(id=student_id)

    print(student_id)

    # Fetch the attendance data for the student
    attendance_data = Attendance.objects.filter(student=student).values('date', 'present')

    # Convert the queryset to a list of dictionaries
    attendance_list = list(attendance_data)

    # Prepare the data for FullCalendar
    events = []
    today = timezone.now().date()
    for record in attendance_list:
        event = {
            'title': 'Present' if record['present'] else 'Absent',
            'start': record['date'].strftime('%Y-%m-%d'),
            'backgroundColor': 'green' if record['present'] else 'red',
            'borderColor': 'green' if record['present'] else 'red',
            'classNames': ['present' if record['present'] else 'absent']
        }
        events.append(event)

    # Add unmarked days
    start_date = attendance_list[0]['date'] if attendance_list else today
    end_date = attendance_list[-1]['date'] if attendance_list else today

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        if not any(event['start'] == date_str for event in events):
            event = {
                'start': date_str,
                'backgroundColor': 'grey',
                'borderColor': 'grey',
                'classNames': ['unmarked']
            }
            events.append(event)
        current_date += timezone.timedelta(days=1)

    return JsonResponse(events, safe=False)
