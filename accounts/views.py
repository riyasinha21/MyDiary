from django.shortcuts import render,get_object_or_404, redirect
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

from accounts.serializers import (
        UserRegistrationSerializer,
        VerifyOTPSerializer,
        UserLoginSerializer,
        ChangePasswordSerializer,
        ProfileSerializer,
        PrivacySettingsSerializer,

    )

from accounts.models import  PendingRegistration, PrivacySettings
from diary.models import DiaryEntry
from community.models import FriendRequest

from .utils import EmailService
from .choices import COUNTRY_CODE_CHOICES

User = get_user_model()


def signup_view(request):
    
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data = request.POST)
        
        if serializer.is_valid():
            
            data = serializer.validated_data
            
            email_service = EmailService(sender=settings.EMAIL_HOST_USER)
            
            # Generate OTP
            otp = email_service.generate_otp()
            
            # Save pending registration
            PendingRegistration.objects.update_or_create(
                email=data["email"],
                defaults={
                    "name": data["name"],
                    "country_code": data["country_code"],
                    "phone_number": data["phone_number"],
                    # During signup
                    "password": make_password(data["password"]),
                    "otp": otp,
                }
            )
            
            # Store email in Django session
            request.session["pending_email"] = data["email"]
            
            # Send OTP email
            email_service.send_otp_mail(
                email=data["email"],
                otp=otp
            )
            
            return redirect("verify_otp")
        
        return render(
            request,
            "signup.html",
            {
                "countries": COUNTRY_CODE_CHOICES,
                "errors" : serializer.errors,
                "data" : request.POST 
            }
        )         
    return render(
        request,
        "signup.html",
        {
            "countries" : COUNTRY_CODE_CHOICES
        }
    )           


def verify_otp_view(request):
    
    email = request.session.get("pending_email")

    if not email:
        return redirect("signup")
        
    if request.method ==  "POST":

        serializer = VerifyOTPSerializer(
            data={
                "email": email,
                "otp": request.POST.get("otp")
            }
        )
        
        if serializer.is_valid():
            
            pending_registration = (
                serializer.validated_data["pending_registration"]
            )
        
            # Create actual User after successful OTP verification
            if User.objects.filter(
                email=pending_registration.email 
            ).exists():
                
                return render(
                    request,
                    "verify_otp.html",
                    {
                        "error": "User is already registered."   
                    }
                )
        
            #check phone number
            if User.objects.filter(
                country_code=pending_registration.country_code,
                phone_number=pending_registration.phone_number
            ).exists():
                
                return render(
                    request,
                    "verify_otp.html",
                    {
                        "error": "Phone number is already registered."
                    }
                )

            # Create actual user
            user = User.objects.create(
                email = pending_registration.email,
                name = pending_registration.name,
                country_code=pending_registration.country_code,
                phone_number = pending_registration.phone_number, 
                password=pending_registration.password,  
                is_verified = True
            )
             
            
            # Delete temporary registration
            pending_registration.delete()
            
            # Remove email from session after successful verification
            request.session.pop("pending_email", None)
            
            return redirect("login")
            
        return render(
            request,
            "verify_otp.html",
            {
                "errors": serializer.errors
            }   
        )
    return render(request, "verify_otp.html")
        
         
def login_view(request):
    
    if request.method == "POST":
        
        serializer = UserLoginSerializer(data=request.POST)
        
    
        if serializer.is_valid():
            
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            
            user = authenticate(
                request,
                email=email, 
                password=password
            )
           
            if user is None:
                
                return render(
                    request,
                    "login.html",
                    {
                        "error" : "Invalid email or password."
                    }
                )
                
            if not user.is_verified:
                return render(
                    request,
                    "login.html",
                    {
                        "error": "Please verify your email first."
                    }
                )
                
            # Create Django session
            login(request, user)
            
            return redirect("home")
        
        return render(
            request,
            "login.html",
            {
                "errors" : serializer.errors
            }
        )
    
    return render(request,"login.html")       

#Change Password
@login_required
def change_password_view(request):

    serializer = ChangePasswordSerializer(
        data=request.POST or None,
        context={"user": request.user}
    )

    errors = None

    if request.method == "POST":

        if serializer.is_valid():
            serializer.save()

            update_session_auth_hash(
                request,
                request.user
            )
            
            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect("change_password")

        errors = serializer.errors

    return render(
        request,
        "change_password.html",
        {
            "errors": errors,
        }
    )                               

@login_required
def profile_view(request):

    # ==========================================
    # COUNTS
    # ==========================================

    diary_count = DiaryEntry.objects.filter(
        user=request.user
    ).count()

    friend_count = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status="accepted"
    ).count()


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":


        # ======================================
        # REMOVE PROFILE IMAGE
        # ======================================

        if request.POST.get("remove_profile_image") == "1":

            old_image = request.user.profile_image

            if old_image:

                if old_image.storage.exists(old_image.name):
                    old_image.storage.delete(old_image.name)

                request.user.profile_image = None

                request.user.save(
                    update_fields=["profile_image"]
                )

            return redirect("profile")


        # ======================================
        # UPLOAD / REPLACE PROFILE IMAGE
        # ======================================

        if request.FILES.get("profile_image"):

            data = request.POST.copy()

            data["profile_image"] = request.FILES.get(
                "profile_image"
            )

            serializer = ProfileSerializer(
                request.user,
                data=data,
                partial=True
            )

            if serializer.is_valid():

                old_image = request.user.profile_image

                serializer.save()

                if old_image and old_image.name != request.user.profile_image.name:

                    if old_image.storage.exists(old_image.name):
                        old_image.storage.delete(old_image.name)

                return redirect("profile")

            return render(
                request,
                "profile.html",
                {
                    "errors": serializer.errors,
                    "edit_mode": False,
                    "diary_count": diary_count,
                    "friend_count": friend_count,
                }
            )


        # ======================================
        # SAVE EDITED PROFILE
        # ======================================

        if request.POST.get("save_profile") == "1":

            data = request.POST.copy()

            data.pop("save_profile", None)

            serializer = ProfileSerializer(
                request.user,
                data=data,
                partial=True
            )

            if serializer.is_valid():

                serializer.save()

                return redirect("profile")

            return render(
                request,
                "profile.html",
                {
                    "errors": serializer.errors,
                    "edit_mode": True,
                    "diary_count": diary_count,
                    "friend_count": friend_count,
                }
            )


    # ==========================================
    # GET
    # ==========================================

    serializer = ProfileSerializer(request.user)

    edit_mode = request.GET.get("edit") == "1"


    return render(
        request,
        "profile.html",
        {
            "profile": serializer.data,
            "edit_mode": edit_mode,
            "diary_count": diary_count,
            "friend_count": friend_count,
        }
    )

def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def home_view(request):

    # Greeting
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"


    # Get public diaries
    public_diaries = DiaryEntry.objects.filter(
        visibility="public"
    ).exclude(
        user=request.user
    ).order_by("-created_at")


    # Add like and bookmark status
    for diary in public_diaries:

        diary.is_liked = diary.likes.filter(
            user=request.user
        ).exists()

        diary.is_bookmarked = diary.bookmarks.filter(
            user=request.user
        ).exists()


    # Render home page
    return render(
        request,
        "home.html",
        {
            "greeting": greeting,
            "public_diaries": public_diaries
        }
    )
    
@login_required
def settings_view(request):
    return render(request, "settings.html")


@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        
        user.delete()
        
        logout(request)
        
        return redirect("login")
    
    return render(
        request,
        "delete_account.html"
    )
    
@login_required
def privacy_view(request):
    
    privacy_settings, created = PrivacySettings.objects.get_or_create(
        user = request.user
    )
        
    if request.method == "POST":

            data = {
                "profile_visibility": request.POST.get("profile_visibility"),
                "friend_request_permission": request.POST.get(
                    "friend_request_permission"
                ),
                "searchable": request.POST.get("searchable") == "on",
            }

            serializer = PrivacySettingsSerializer(
                privacy_settings,
                data=data
            )

            if serializer.is_valid():
                serializer.save()
                return redirect("privacy")

    else:
        serializer = PrivacySettingsSerializer(
            privacy_settings
        )
    
        return render(
            request,
            "privacy.html",
            {
                "serializer": serializer,
            }
        )
        
@login_required
def user_profile_view(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    
    diary_count = DiaryEntry.objects.filter(
        user = user,
        visibility="public"
    ).count()
    
    friend_count = FriendRequest.objects.filter(
        Q(sender=user) | Q(receiver=user),
        status="accepted"
    ).count()
    
    return render(
        request,
        "user_profile.html",
        {
            "profile_user": user,
            "diary_count": diary_count,
            "friend_count": friend_count,
        }
    )



