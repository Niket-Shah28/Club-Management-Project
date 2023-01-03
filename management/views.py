from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.views import APIView
from .models import USER
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login,authenticate,logout
from .forms import SignIn
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .decoraters import *
from django.utils.decorators import method_decorator
from rest_framework import mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.core import serializers
import razorpay

"""
superuser: niketshah@gmail.com 
password: Niket 
"""
# Create your views here.

#This functions allows user to sign in
@csrf_exempt
def signin(request):
    if request.method=='POST':
        email=request.POST['Email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("You are logged in")
        else:
            return HttpResponse("Invalid Details")

#This function allows user to sihgn out
def signout(request):
    logout(request)
    return HttpResponse("You are logged out")


#Any User can add his/her details online and register and get verified

class Register(APIView):
    def post(self,request,format=None):
        serializer1=usermodel(data=request.data)
        if serializer1.is_valid():
            account=serializer1.save()
        user2=serializer1.data
        user=USER.objects.get(email=account.email)
        try:
            token = Token.objects.get(user_id=user.id)

        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        name=USER.objects.get(email=account.email)
        send_mail(
            subject='Hello Welcome to django email verification',
            message='Hi '+name.First_Name+
            ' ,I am from Mumbai Suburban Club,thank you for registering.'+
            'This is your link to verify http://127.0.0.1:8000/verify/'+str(token),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[user,]
        )
        return Response({'user_data':user2})

        # http://127.0.0.1:8000/


#This function is used during email verification and verifies the user as soon as link is clicked
def verification(request,token):
    user_email=Token.objects.get(key=token)
    user_details=USER()
    try:
        user_details=USER.objects.get(email=user_email.user)
    except:
        return HttpResponse("ERROR")
    if user_details:
        token=Token.objects.get(key=user_email)
        token.delete()
        Token.objects.create(user=USER.objects.get(email=user_details.email))
        user_details.is_verified=True
        user_details.save()
        return HttpResponse("You are Verified")

#Manager is only entered by superuser and contains its own manager id  
@csrf_exempt
def add_manager(request):
    if request.method=='POST':
        manager_email=request.POST['email']
        manager_data_possible=Manager()
        manager_data_possible.Manager_email=USER.objects.get(email=manager_email)
        manager_data_possible.is_manager=True
        user=USER.objects.get(email=manager_email)
        if user.is_verified:
            user.is_staff=True
            user.save()
            if manager_data_possible:
                manager_data_possible.save()
                return HttpResponse("Hello Manager")
            else:
                return HttpResponse("Invalid Data")
        else:
            return HttpResponse("Invalid User")

#This class is used to update the manager data and only superuser has its right
class Manager_update(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def put(self,request,id,format=None):
        manager_email=request.POST['email']
        manager_status=request.POST['status']
        manager_data_possible=Manager.objects.get(manager_id=id)
        manager_data_possible.Manager_email=USER.objects.get(email=manager_email)
        manager_data_possible.is_manager=manager_status
        if manager_data_possible :
            manager_data_possible.save()
            return HttpResponse("Manager Updated")
        else:
            return HttpResponse("Invalid Data")

    def delete(self,request,id,format=None):
        manager_data_possible=Manager.objects.get(manager_id=id)
        manager_data_possible.delete()
        return HttpResponse("Manager Deleted")

#this function is used to add staff and only manager has its right
# It collecets the data from form 
@csrf_exempt
def add_staff(request):
    if(request.method=='POST'):
        staff_email=request.POST['email']
        staff_type=request.POST['Type']
        Staff=NormalStaff()
        Staff.Staff_email=USER.objects.get(email=staff_email)
        Staff.Staff_role=staff_type
        Staff.is_Staff=True
        user=request.user
        user_id=Manager.objects.get(Manager_email=user)
        Staff.manager_id=Manager.objects.get(manager_id=user_id.manager_id)
        user1=USER.objects.get(email=staff_email)
        if user1.is_verified:
            if Staff:
                Staff.save()
                return HttpResponse("Hello Staff")
            else:
                return HttpResponse("Invalid Details")
        else:
            return HttpResponse("Invalid User")
        
#This class is used to modify Staff data and only manager has its rights
class Modify_Staff(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def put(self,request,id,format=None):
        staff_email=request.POST['email']
        staff_Type=request.POST['Type']
        staff_presence=request.POST['present']
        Staff_data=NormalStaff.objects.get(Staff_id=id)
        Staff_data.Staff_email=USER.objects.get(email=staff_email)
        Staff_data.Staff_role=staff_Type
        Staff_data.is_staff=staff_presence
        user1=Manager.objects.get(Manager_email=request.user)
        if user1.is_manager:
            if Staff_data:
                Staff_data.save()
                return HttpResponse("Staff Updated")
            else:
                return HttpResponse("Invalid Data")
        else:
            return HttpResponse("Manager Requied")
    
    def delete(self,request,id,format=None):
        user1=Manager.objects.get(Manager_email=request.user)
        if user1.is_manager:
            Staff_data=NormalStaff.objects.get(Staff_id=id)
            Staff_data.delete()
            return HttpResponse("Staff Deleted")
        else:
            return HttpResponse("Manager Required")


#This is used to add activities and only staff can do it
@csrf_exempt
def add_activity(request):
    if request.method=='POST':
        activity_name=request.POST['activity_name']
        activity_presence=request.POST['presence']
        activity_data=activities()
        activity_data.activity_name=activity_name
        activity_data.is_present=activity_presence
        user=request.user
        staff_data=NormalStaff.objects.get(Staff_email=user)
        activity_data.staff_id=NormalStaff.objects.get(Staff_email=user)
        if user.is_verified:
            if staff_data.is_staff:
                if activity_data:
                    activity_data.save()
                    return HttpResponse("Activity added")
                else:
                    return HttpResponse("Invalid Data")
            else:
                return HttpResponse("Staff Required")
        else:
            return HttpResponse("Invalid User")


#The below class is used to modify the activity data
class Modify_Activity(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def put(self,request,id,format=None):
        activity_name=request.POST['activity_name']
        activity_presence=request.POST['presence']
        activity_data=activities.objects.get(activity_id=id)
        activity_data.activity_name=activity_name
        activity_data.is_present=activity_presence
        user1=NormalStaff.objects.get(Staff_email=request.user)
        if user1.is_staff:
            if activity_data:
                activity_data.save()
                return HttpResponse("Activity Updated")
            else:
                return HttpResponse("Invalid Data")
        else:
            return HttpResponse("Staff Required")

    def delete(self,request,id,format=None):
        user1=NormalStaff.objects.get(Staff_email=request.user)
        if user1.is_staff:
            activity_data=activities.objects.get(activity_id=id)
            activity_data.delete()
            return HttpResponse("Activity Deleted")
        else:
            return HttpResponse("Staff Required")


# This add the price for members and only staff hads its access
@csrf_exempt
def add_Member_price(request,id):
    if request.method=='POST':
        activity_price=request.POST['price']
        holiday=request.POST['holiday_presence']
        member_price=Price_for_members()
        member_price.activity_price=activity_price
        member_price.for_holiday=holiday
        member_price.activity_id=activities.objects.get(activity_id=id)
        user=request.user
        member_price.Staff_id=NormalStaff.objects.get(Staff_email=user)
        user_online=NormalStaff.objects.get(Staff_email=user)
        if user_online.is_staff:
            if member_price:
                member_price.save()
                return HttpResponse('Member Price Updated')
            else:
                return HttpResponse("Invalid data")
        else:
            return HttpResponse("Staff required")

# this class modifies the member price data and staff has its access
class Member_price_Modify(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def put(self,request,id,format=None):
        activity_price=request.POST['price']
        holiday=request.POST['holiday_presence']
        member_Price_data=Price_for_members.objects.get(member_price_id=id)
        member_Price_data.activity_price=activity_price
        member_Price_data.for_holiday=holiday
        user1=NormalStaff.objects.get(Staff_email=request.user)
        if user1.is_staff:
            if member_Price_data:
                member_Price_data.save()
                return HttpResponse("Member Price Modified")
            else:
                return HttpResponse("Invalid data")
        else:
            return HttpResponse("Staff Required")

    def delete(self,request,id,format=None):
        user1=NormalStaff.objects.get(Staff_email=request.user)
        if user1.is_staff:
            member_Price_data=Price_for_members.objects.get(member_price_id=id)
            member_Price_data.delete()
            return HttpResponse("Member Price Deleted")
        else:
            return HttpResponse("Staff Required")

#this add guest price and staff has its access
@csrf_exempt
def add_Guest_price(request,id):
    if request.method=='POST':
        activity_price=request.POST['price']
        holiday=request.POST['holiday_presence']
        guest_price=Price_for_Guests()
        guest_price.activity_price=activity_price
        guest_price.for_holiday=holiday
        guest_price.activity_id=activities.objects.get(activity_id=id)
        user=request.user
        guest_price.Staff_id=NormalStaff.objects.get(Staff_email=user)
        user_online=NormalStaff.objects.get(Staff_email=user)
        if user_online.is_staff:
            if guest_price:
                guest_price.save()
                return HttpResponse('Guest Price Updated')
            else:
                return HttpResponse("Invalid data")
        else:
            return HttpResponse("Staff required")

# Same goes here this modifies the guest price data and staff has its access
class Guest_price_Modify(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def put(self,request,id,format=None):
        activity_price=request.POST['price']
        holiday=request.POST['holiday_presence']
        Guest_Price_data=Price_for_Guests.objects.get(Guest_price_id=id)
        Guest_Price_data.activity_price=activity_price
        Guest_Price_data.for_holiday=holiday
        user1=NormalStaff.objects.get(Staff_email=request.user)
        print(request.user)
        if user1.is_staff:
            if Guest_Price_data:
                Guest_Price_data.save()
                return HttpResponse("Guest Price Modified")
            else:
                return HttpResponse("Invalid data")
        else:
            return HttpResponse("Staff Required")

    def delete(self,request,id,format=None):
        Guest_Price_data=Price_for_Guests.objects.get(Guest_price_id=id)
        user1=NormalStaff.objects.get(Staff_email=request.user)
        if user1.is_staff:
            Guest_Price_data.delete()
            return HttpResponse("Guest Price Deleted")
        else:
            return HttpResponse("Staff Required")


#This adds membership types and its prices and staff has its access
@csrf_exempt
def add_memberships(request):
    if request.method=='POST':
        membership_type=request.POST['membership_type']
        membership_price=request.POST['price']
        memberships=memberships_and_price()
        memberships.membership_type=membership_type
        memberships.membership_price=membership_price
        user_online=NormalStaff.objects.get(Staff_email=request.user)
        memberships.Staff_id=NormalStaff.objects.get(Staff_email=request.user)
        if user_online.is_staff:
            if memberships:
                memberships.save()
                return HttpResponse("Memberhsip Data Saved")
            else:
                return HttpResponse("Invalid Data")
        else:
            return HttpResponse("Staff Required")

#This class is used to modify the memberships and price data
class Modify_memberships(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]
    
    def put(self,request,id,format=None):
        membership_type=request.POST['membership_type']
        membership_price=request.POST['price']
        memberships=memberships_and_price.objects.get(membership_data_id=id)
        memberships.membership_type=membership_type
        memberships.membership_price=membership_price
        user_online=NormalStaff.objects.get(Staff_email=request.user)
        memberships.Staff_id=NormalStaff.objects.get(Staff_email=request.user)
        if user_online.is_staff:
            if memberships:
                memberships.save()
                return HttpResponse("Memberhsip Data Updated")
            else:
                return HttpResponse("Invalid Data")
        else:
            return HttpResponse("Staff Required")

    def delete(self,request,id,format=None):
        user_online=NormalStaff.objects.get(Staff_email=request.user)
        memberships=memberships_and_price.objects.get(membership_data_id=id)
        if user_online.is_staff:
            memberships.delete()
            return HttpResponse("Membership Data Deleted")
        else:
            return HttpResponse("Staff Required")

#This gives us the list of all users and only manager has its access
class Users(ListView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    model=USER

    def get(self,request,format=None):
        try:
            manager_data=Manager.objects.get(Manager_email=request.user)
        except Exception as e :
            return HttpResponse(e)
        if manager_data:
            if manager_data.is_manager:
                users=USER.objects.all()
                users=users.order_by('id')
                data=serializers.serialize('json',users)
                return JsonResponse(data,safe=False)


#This functions send smail to person who requests for Password Reset
def Password_reset(request):
    if request.method=='GET':
        try:
            user_details=USER.objects.get(email=request.user)
        except Exception as e:
            return HttpResponse(e)
        user_token=Token.objects.get(user=USER.objects.get(email=request.user))
        send_mail(
            subject='Password Reset',
            message='Hi '+user_details.First_Name+
            ' ,This is link for Your Password Reset.'+
            ' http://127.0.0.1:8000/password-reset/'+str(user_token.key),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[user_details.email,]
        )
        return HttpResponse("Check Your Mail")

#After Clicking on link a form will be popped and from that the data will be verified and password will be changed
class Mail_Password_Reset(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated,]

    def post(self,request,token,format=None):
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            user_token=Token.objects.get(key=token)
            user_details=USER.objects.get(email=user_token.user)
            user_details.set_password(confirm_password)
            user_token=Token.objects.get(key=token)
            if user_details:
                user_details.save()
            else:
                return HttpResponse("Invalid Data")
            user_token.delete()
            Token.objects.create(user=USER.objects.get(email=user_details.email))
            return HttpResponse("Token Updated and password reset")
        else:
            return HttpResponse("Both the fields does not match")

@csrf_exempt
def add_member(request):
    if request.method=='POST':
        email=request.POST['email']
        member_details=Member()
        member_details.Member_email=USER.objects.get(email=email)
        try:
            member_details.Staff_id=NormalStaff.objects.get(Staff_email=request.user)
        except Exception as e:
            return HttpResponse(e)
        if member_details:
            member_details.save()
           # member_id=Member.objects.get(Member_email=USER.objects.get(email=email))
            return HttpResponse("Here member's data is saved and then is redirected to adding")
        else:
            return HttpResponse("Invalid Data")

@csrf_exempt
def adding_membership(request,id):
    if request.method=='POST':
        membership_type=request.POST['type']
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        Payment_type=request.POST['payment_type']
        Payment_date=request.POST['payment_date']
        Membership_details=Current_Member_Membership()
        Membership_details.member_id=Member.objects.get(Member_id=id) 
        Membership_details.membership_type_id=memberships_and_price.objects.get(membership_type=membership_type)
        Membership_details.start_date=start_date   
        Membership_details.end_date=end_date       
        Membership_details.Payment_type=Payment_type
        Membership_details.Payment_date=Payment_date
        amount=memberships_and_price.objects.get(membership_type=membership_type)
        Membership_details.Amount=amount.membership_price
        try:
            Membership_details.Staff_id=NormalStaff.objects.get(Staff_email=request.user)
        except Exception as e:
            return HttpResponse("Staff Required")
        if Membership_details:
            Membership_details.save()
            return HttpResponse("Member Membership data is saved here and is directed to Payment Gateway")
        else:
            return HttpResponse("Invalid Details")

@csrf_exempt
def member_payment(request,id):
        client = razorpay.Client(auth=("rzp_test_Ca0278JPABNPT5", "w1k8Lum4gemGAQR3nU8u97j9"))

        member_details=Member.objects.get(Member_id=id)
        member_membership_details=Current_Member_Membership.objects.get(member_id=id)
        membership_type=member_membership_details.membership_type_id
        membership_details=memberships_and_price.objects.get(membership_data_id=membership_type)
        amount=membership_details.membership_price
        Total_amount=amount*100
        order_currency='INR'
        payment=client.order.create({'amount':Total_amount,'currency':'INR','payment_capture':1})

        return render(request,'payment.html',{'payment':payment})

@csrf_exempt
def success(request):
    return HttpResponse("Your Payment Was Successful")


