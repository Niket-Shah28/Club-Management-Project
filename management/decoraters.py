import functools
from .models import *
from django.shortcuts import HttpResponse,redirect


def staff_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        emails=NormalStaff.objects.all()
        if request.user not in emails.Staff_name:
            return HttpResponse("Staff Required")
    return wrapper

def admin_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_emails=USER.objects.filter(is_admin=True)
        if not request.user in admin_emails:
            return HttpResponse("Admin Required")
        return redirect('')
    return wrapper

def manager_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        manager_emails=Manager.objects.get(Manager_email=request.user)
        print(request.user)
        if manager_emails:
            return ('/')
        else:
            return HttpResponse("Manager Required")
    return wrapper    