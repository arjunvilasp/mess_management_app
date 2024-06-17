from django.db import models
from django.utils import timezone
# Create your models here.


class Admin(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Student(models.Model):
    username = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    room_no = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.student.username} - {self.date} ({'Present' if self.present else 'Absent'})"
    
    
class Bill(models.Model):

    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.username} - {self.month} - {self.amount}"
    

class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.IntegerField(default=0)

    def __str__(self):
        return f'Complaint from {self.student.username} at {self.timestamp}'
    



class Meal(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    MEAL_TYPES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Tea', 'Tea'),
        ('Dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(choices=MEAL_TYPES, max_length=20)
    day = models.CharField(choices=DAY_CHOICES, max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.type} ({self.day})"

    class Meta:
        unique_together = ('day', 'type')


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal_types = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    stud_id = models.CharField(max_length=255)



class LeaveRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.IntegerField(default=0)
    seen = models.IntegerField(default=0)
    admin_seen = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.date}"


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.username} - {self.get_rating_display()}"
    
