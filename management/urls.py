from django.urls import path
from . import views

urlpatterns=[
    path("register/",views.Register.as_view(),name='request'),
    path("verify/<token>",views.verification,name='verification'),
    path("signin",views.signin,name='signin'),
    path("signout",views.signout,name='signout'),
    path("manager",views.add_manager,name='manager'),
    path("managerupdate/<id>",views.Manager_update.as_view(),name='manager_update'),
    path("addstaff",views.add_staff,name='staff'),
    path("modifystaff/<id>",views.Modify_Staff.as_view(),name='staff_modify'),
    path("addactivity",views.add_activity,name='activity'),
    path('modifyactivity/<id>',views.Modify_Activity.as_view(),name='modifyactivity'),
    path('addmemberprice/<id>',views.add_Member_price,name='memberprice'),
    path('modifymemberprice/<id>',views.Member_price_Modify.as_view(),name='modifymemberprice'),
    path("addguestprice/<id>",views.add_Guest_price,name='guestprice'),
    path("modifyguestprice/<id>",views.Guest_price_Modify.as_view(),name="modifyguestprice"),
    path("addmembership",views.add_memberships,name='membership'),
    path("modifymembership/<id>",views.Modify_memberships.as_view(),name='modifymembership'),
    path("Listofusers",views.Users.as_view(),name='users_list'),
    path("passwordreset/<token>",views.Password_reset,name='password_reset'),
    path("password-reset/<token>",views.Mail_Password_Reset.as_view(),name='mail_password_reset'),
    path('addmember',views.add_member,name='add_member'),
    path('addmembership/<id>',views.adding_membership,name='add_membership'),
    path('payment/<id>',views.member_payment,name='payment'),
    path('success',views.success,name='success_payment')
]