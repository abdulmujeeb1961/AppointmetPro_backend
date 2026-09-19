from apps.users.views.login_views import LoginView
from apps.users.views.logout_views import LogoutView
from apps.users.views.ChangePassword_views import ChangePasswordView
from django.urls import path
from apps.users.views.ForgotPassword_views import ForgotPasswordView
from apps.users.views.ResetPassword_views import ResetPasswordView
from apps.users.views.usercreate_views import UserCreateView


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('auth/forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('auth/resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
     path('auth/usercreatepassword/', UserCreateView.as_view(), name='usercreatepassword'),
    
    
    
]