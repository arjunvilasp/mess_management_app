# custom_context_processors.py
from .models import LeaveRequest, Complaint


def custom_context(request):

    leave_requests = LeaveRequest.objects.select_related('student').filter(admin_seen=0)
    complaints = Complaint.objects.select_related('student').filter(seen=0)


    return {
        'leave_requests': leave_requests,
        'complaints':complaints
    }
