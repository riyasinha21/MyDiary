from django.urls import path

from .views import (
    signup_view,
    verify_otp_view,
    login_view,
    profile_view,
    logout_view,
    home_view,
    settings_view,
    change_password_view,
    delete_account_view,
    privacy_view,
    user_profile_view,
)

from .template_views import (
    dashboard_page,
    
)


urlpatterns = [

    # =========================
    # HTML / NORMAL DJANGO VIEWS
    # =========================

    path("signup/", signup_view, name="signup"),

    path("verify-otp/",verify_otp_view, name="verify_otp"),

    path("login/", login_view, name="login"),
        
    path("profile/",profile_view, name="profile"),
    
    path("profile/<int:user_id>/", user_profile_view, name="user_profile"),
    
    path("logout/", logout_view, name="logout"),

    # =========================
    # OTHER PAGES
    # =========================

    path("dashboard/", dashboard_page, name="dashboard"),

    path("home/", home_view, name="home"),
    
    path("settings/", settings_view, name="settings"),
    
    path("settings/change-password/", change_password_view, name="change_password"),
    
    path("settings/delete-account/", delete_account_view, name = "delete_account"),
    
    path("privacy/", privacy_view, name="privacy" ),
    
  
]