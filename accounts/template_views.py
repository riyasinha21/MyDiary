from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

def signup_page(request):
    return render(request, "signup.html")

def verify_otp_page(request):
    return render(request, "verify_otp.html")

def login_page(request):
    return render(request, "login.html")

def dashboard_page(request):
    return render(request, "dashboard.html")





