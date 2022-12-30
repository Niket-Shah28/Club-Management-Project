from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(USER)
class useradmin(admin.ModelAdmin):
    list_display=('First_Name','Middle_Name','Last_Name','password','Gender','Salutation','email','Contact_no',
                    'Emergency_contact_no','Date_of_Birth','Address_line_1','Address_line_2','State','City',
                    'Pincode','Id_Proof_name','Id_Proof_no','is_staff','is_verified','is_superuser')

@admin.register(NormalStaff)
class useradmin(admin.ModelAdmin):
    list_display=('Staff_id','Staff_email','Staff_role','is_staff','manager_id')

@admin.register(Manager)
class useradmin(admin.ModelAdmin):
    list_display=('manager_id','Manager_email','is_manager')

@admin.register(Member)
class useradmin(admin.ModelAdmin):
    list_display=('Member_id','Member_email','is_member','Staff_id')

@admin.register(memberships_and_price)
class membership(admin.ModelAdmin):
    list_display=('membership_data_id','membership_type','membership_price','Staff_id')

@admin.register(Current_Member_Membership)
class membership(admin.ModelAdmin):
    list_display=('member_id','membership_type_id','membership_no','start_date','end_date','Payment_type',
    'Payment_date','Amount','Staff_id')

@admin.register(Member_Membership)
class membership(admin.ModelAdmin):
    list_display=('member_id','membership_type_id','membership_no','start_date','end_date','Payment_type',
    'Payment_date','Amount','Staff_id')

@admin.register(activities)
class activities(admin.ModelAdmin):
    list_display=('activity_id','activity_name','staff_id','is_present')

@admin.register(Price_for_members)
class activities(admin.ModelAdmin):
    list_display=('member_price_id','activity_id','activity_price','for_holiday','Staff_id')

@admin.register(Price_for_Guests)
class activities(admin.ModelAdmin):
    list_display=('Guest_price_id','activity_id','activity_price','for_holiday','Staff_id')

@admin.register(InoutEntry)
class In_Out(admin.ModelAdmin):
    list_display=('InoutEntryid','Date','Time','membership_no','No_of_Guests','Total_Amount','Payment_method',
    'Staff_id','Entered_date')

@admin.register(InoutDetails)
class In_Out(admin.ModelAdmin):
    list_display=('InoutDetailsId','InoutEntryid','Activity_id','member_rate_id','member_amount','Guest_count',
    'Guest_rate_id','Guest_Amount','Total_Activity_amount')