from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

#Q is a Django object used for building complex database queries, especially when you need OR conditions.
from django.db.models import Q
from .models import FriendRequest, Notification
from diary.models import DiaryEntry, DiaryLike, DiaryComment, DiaryBookmark 


User = get_user_model()



@login_required
def community_view(request):

     # All users except the logged-in user
    users = User.objects.exclude(
        id=request.user.id
    ).order_by("name")

    # Get accepted friends
    accepted_requests = FriendRequest.objects.filter(
        status="accepted"
    ).filter(
        Q(sender=request.user) |
        Q(receiver=request.user)
    )

    friends = []

    for friend_request in accepted_requests:

        if friend_request.sender == request.user:
            friends.append(friend_request.receiver)
        else:
            friends.append(friend_request.sender)
            
    # ==========================================
    # RECEIVED PENDING FRIEND REQUESTS
    # ==========================================

    friend_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status="pending"
    ).select_related(
        "sender"
    )


    # ==========================================
    # SUGGESTED USERS
    # ==========================================

    # Get IDs of accepted friends
    friend_ids = [
        friend.id
        for friend in friends
    ]


    # Get IDs of users who sent a pending request
    request_sender_ids = friend_requests.values_list(
        "sender_id",
        flat=True
    )


    # Suggested users
    suggested_users = users.exclude(
        id__in=friend_ids
        ).exclude(
            id__in=request_sender_ids
        )

    for user in suggested_users:

        friend_request = FriendRequest.objects.filter(
            sender=request.user,
            receiver=user,
            status="pending"
        ).first()

        user.friend_request_status = None
        user.friend_request_direction = None
        user.friend_request_id = None

        if friend_request:

            user.friend_request_status = "pending"
            user.friend_request_direction = "sent"
            user.friend_request_id = friend_request.id


    return render(
        request,
        "community.html",
        {
            "users": suggested_users,
            "friend_requests": friend_requests,
            "friends": friends,
        }
    )


# SEND FRIEND REQUEST

@login_required
def send_friend_request_view(request, user_id):

    receiver = get_object_or_404(
        User,
        id=user_id
    )

    # Prevent sending request to yourself
    if receiver == request.user:
        return redirect("community")

    if request.method == "POST":

        friend_request, created = FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )
        
        if created:
            
            Notification.objects.create(
                recipient=receiver,
                sender=request.user,
                notification_type="friend_request"
            )
    return redirect("community")

@login_required
def accept_friend_request_view(request,request_id):
    
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status="pending"
    )

    if request.method == "POST":

        friend_request.status = "accepted"
        friend_request.save()
        
        Notification.objects.create(
            recipient=friend_request.sender,
            sender=request.user,
            notification_type="friend_accepted"
        )

    return redirect("community")

@login_required
def decline_friend_request_view(request, request_id):
    
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status="pending"
    )
    
    if request.method == "POST":
        
        friend_request.delete()
        
        
        
    return redirect("community")

@login_required
def remove_friend_view(request, user_id):
    
    friend = get_object_or_404(
        User,
        id=user_id
    )
    
    if request.method == "POST":
        friend_request = FriendRequest.objects.filter(
            Q(sender=request.user, receiver=friend)|
            Q(sender=friend,receiver=request.user),
            status="accepted"
        ).first()
        
        if friend_request:
            
            friend_request.delete()
    
    return redirect("community")
         
#Cancel sending friend request
@login_required
def cancel_friend_request(request, request_id):

    if request.method == "POST":

        friend_request = get_object_or_404(
            FriendRequest,
            id=request_id,
            sender=request.user,
            status="pending"
        )

        friend_request.delete()

    return redirect("community")

@login_required
def community_profile_view(request, user_id):
    
    profile_user = get_object_or_404(
        User,
        id=user_id
    )
    
    if profile_user == request.user:
        return redirect("profile")
    
    # Check if they are already friends
    friendship = FriendRequest.objects.filter(
        Q( sender = request.user, receiver = profile_user) |
        Q(sender = profile_user,receiver = request.user),
        status="accepted"
    ).first()
    
    #check if I sent  a pending request
    sent_request = FriendRequest.objects.filter(
        sender = request.user,
        receiver = profile_user,
        status = "pending"
    ).first()
    
    #check if the person send me a pending request
    received_request = FriendRequest.objects.filter(
        sender = profile_user,
        receiver = request.user,
        status = "pending"
    ).first()
    
    #public diaries
    public_diaries = DiaryEntry.objects.filter(
        user = profile_user,
        visibility="public"
    ).order_by("created_at")
    
    for diary in public_diaries:
        
        diary.is_liked = DiaryLike.objects.filter(
            diary=diary,
            user=request.user
        ).exists()
        
        diary.is_bookmarked = DiaryBookmark.objects.filter(
            diary=diary,
            user=request.user
        ).exists()
    
    #count
    diary_count = public_diaries.count()
    
    friend_count = FriendRequest.objects.filter(
        Q(sender=profile_user) | Q(receiver=profile_user),
        status="accepted"
    ).count()
    
    return render(
        request,
        "community_profile.html",
        {
            "profile_user" : profile_user,
            "friendship" : friendship,
            "sent_request" : sent_request,
            "received_request" : received_request,
            "public_diaries" : public_diaries,
            "diary_count" : diary_count,
            "friend_count" : friend_count
            
        }
    )


#Notification
@login_required
def notification_view(request):
    
    notifications = Notification.objects.filter(
        recipient = request.user
    ).order_by("-created_at")
    
    unread_notification_count = notifications.filter(
        is_read=False
    ).count()
    
    notifications.filter(
        is_read = False
    ).update(
        is_read = True
    )
    
    return render(
        request,
        "notification.html",
        {
            "notifications" : notifications,
            "unread_notification_count": unread_notification_count,
        }
    )
    
@login_required
def notification_redirect_view(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    # Mark notification as read
    notification.is_read = True
    notification.save()

    # Notifications related to a diary
    if notification.diary:

        return redirect(
            "diary_detail",
            id=notification.diary.id
        )

    # Friend request notification
    if notification.notification_type == "friend_request":

        return redirect("community")

    # Friend accepted notification
    if notification.notification_type == "friend_accepted":

        return redirect("community")

    # Default fallback
    return redirect("home")