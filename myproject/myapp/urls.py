from django.urls import path
from .views import  ( StudentDetailsView , SignupView  , loginView , verifyOTPView 
                     , forgotPasswordView, resetPasswordView , logoutView , Updatepassword ,
                     ResendOTPView )
urlpatterns = [
    path('students/', StudentDetailsView.as_view(), name='student-details'), 
    path('students/<int:pk>/', StudentDetailsView.as_view(), name='student-details-update'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('login/', loginView.as_view(), name='login'), 
    path('verifyotp/', verifyOTPView.as_view() , name='verify-otp'),
    path('forgot-password/', forgotPasswordView.as_view() , name='forgot-password'),    
    path('reset-password/', resetPasswordView.as_view() , name='reset-password'),
    path('logout/', logoutView.as_view() , name='logout'),
    path('update-password/', Updatepassword.as_view() , name='update-password'),
    path('resend-otp/', ResendOTPView.as_view() , name='resend-otp'),
    path('search-students/',StudentSearch)
]
