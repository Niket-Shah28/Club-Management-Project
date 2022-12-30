from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
gender_choice=(
    ("UNKNOWN","Unknown"),
    ("MALE","Male"),
    ("FEMALE","Female"),
    ("OTHER","Other"),
)
salutation_choice=(
    ("MR","Mr."),
    ("MASTER","Mst."),
    ("MISS","Ms."),
    ("MRS","Mrs."),
)
id_proof_choice=(
    ("AADHAR CARD","Aadhar Card"),
    ("PAN CARD","Pan Card"),
    ("PASSPORT","Passport"),
)
staff_role_choice=(
    ("RECEPTIONIST","Receptionist"),
    ("LIFE GUARD","Life Guard"),
    ("CLEANER","Cleaner"),
    ("HOUSE KEEPER","House Keeper"),
)
membership_type=(
    ("ANNUAL","Annual"),
    ("6 MONTHS","6 Months"),
    ("3 MONTHS","3 Months"),
)
class USER(AbstractBaseUser,PermissionsMixin):

    objects=CustomUserManager()

    First_Name=models.CharField(max_length=50,blank=False)
    Middle_Name=models.CharField(max_length=50)
    Last_Name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    Gender=models.CharField(max_length=40,choices=gender_choice,default="UNKNOWN")
    Salutation=models.CharField(max_length=40,choices=salutation_choice)
    email=models.EmailField(unique=True)
    Contact_no=PhoneNumberField()
    Emergency_contact_no=PhoneNumberField()
    Date_of_Birth=models.DateField(null=True)
    Address_line_1=models.CharField(max_length=300)
    Address_line_2=models.CharField(max_length=300)
    State=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    Pincode=models.IntegerField(null=True)
    Id_Proof_name=models.CharField(max_length=40,choices=id_proof_choice,default="AADHAR CARD")
    Id_Proof_no=models.CharField(max_length=100)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)

    USERNAME_FIELD='email'

    def __str__(self):
        return self.email
        
class Manager(models.Model):
    manager_id=models.IntegerField(auto_created=True,primary_key=True)
    Manager_email=models.ForeignKey(USER,on_delete=models.CASCADE)
    is_manager=models.BooleanField(default=True)

class NormalStaff(models.Model):
    Staff_id=models.IntegerField(auto_created=True,primary_key=True)
    Staff_email=models.ForeignKey(USER,on_delete=models.CASCADE)
    Staff_role=models.CharField(max_length=40,choices=staff_role_choice,default=None)
    manager_id=models.ForeignKey(Manager,on_delete=models.CASCADE,blank=False)
    is_staff=models.BooleanField(default=True)

    def __int__(self):
        return self.Staff_id

class Member(models.Model):
    Member_id=models.IntegerField(auto_created=True,primary_key=True)
    Member_email=models.ForeignKey(USER,on_delete=models.CASCADE)
    is_member=models.BooleanField(default=True)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE,blank=True)

class memberships_and_price(models.Model):
    membership_data_id=models.IntegerField(auto_created=True,primary_key=True)
    membership_type=models.CharField(max_length=40,choices=membership_type)
    membership_price=models.IntegerField()
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)

class activities(models.Model):
    activity_name=models.CharField(max_length=50)
    activity_id=models.IntegerField(auto_created=True,primary_key=True)
    staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)
    is_present=models.BooleanField(default=True)

    def __int__(self):
        return self.activity_id

class Price_for_members(models.Model):
    member_price_id=models.IntegerField(auto_created=True,primary_key=True)
    activity_id=models.ForeignKey(activities,on_delete=models.CASCADE)
    activity_price=models.IntegerField()
    for_holiday=models.BooleanField(default=False)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)

class Price_for_Guests(models.Model):
    Guest_price_id=models.IntegerField(auto_created=True,primary_key=True)
    activity_id=models.ForeignKey(activities,on_delete=models.CASCADE)
    activity_price=models.IntegerField()
    for_holiday=models.BooleanField(default=False)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)

class Current_Member_Membership(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.CASCADE)
    membership_type_id=models.ForeignKey(memberships_and_price,on_delete=models.CASCADE)
    membership_no=models.IntegerField(primary_key=True)
    start_date=models.DateField(auto_now_add=False)
    end_date=models.DateField(auto_now_add=False)
    Payment_type=models.CharField(max_length=100)
    Payment_date=models.DateField(auto_now_add=False)
    Amount=models.IntegerField(blank=True)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)

class Member_Membership(models.Model):
    member_id=models.ForeignKey(Member,on_delete=models.CASCADE)
    membership_type_id=models.ForeignKey(memberships_and_price,on_delete=models.CASCADE)
    membership_no=models.ForeignKey(Current_Member_Membership,on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=False)
    end_date=models.DateField(auto_now_add=False)
    Payment_type=models.CharField(max_length=100)
    Payment_date=models.DateField(auto_now_add=False)
    Amount=models.IntegerField(blank=True)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)

class InoutEntry(models.Model):
    InoutEntryid=models.IntegerField(auto_created=True,primary_key=True)
    Date=models.DateField(auto_now_add=True)
    Time=models.TimeField(auto_now_add=True)
    membership_no=models.ForeignKey(Current_Member_Membership,on_delete=models.CASCADE,blank=False)
    No_of_Guests=models.IntegerField()
    Total_Amount=models.IntegerField(blank=True)
    Payment_method=models.CharField(max_length=100)
    Staff_id=models.ForeignKey(NormalStaff,on_delete=models.CASCADE)
    Entered_date=models.DateField(auto_now_add=True)

class InoutDetails(models.Model):
    InoutDetailsId=models.IntegerField(auto_created=True,primary_key=True)
    InoutEntryid=models.ForeignKey(InoutEntry,on_delete=models.CASCADE)
    Activity_id=models.ForeignKey(activities,on_delete=models.CASCADE)
    member_rate_id=models.ForeignKey(Price_for_members,on_delete=models.CASCADE)
    member_amount=models.IntegerField(blank=True)
    Guest_count=models.IntegerField(blank=True)
    Guest_rate_id=models.ForeignKey(Price_for_Guests,on_delete=models.CASCADE)
    Guest_Amount=models.IntegerField(blank=True)
    Total_Activity_amount=models.IntegerField(blank=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
