from django.urls import path

from .views import (
    community_view ,
    community_profile_view,
    send_friend_request_view,
    notification_view,
    accept_friend_request_view ,
    decline_friend_request_view ,
    remove_friend_view,
    cancel_friend_request,
    notification_redirect_view
)


urlpatterns = [

    path(
        "",
        community_view,
        name="community"
    ),
    
    path(
        "profile/<int:user_id>/",
        community_profile_view,
        name="community_profile"
    ),

    path(
        "friend-request/<int:user_id>/",
        send_friend_request_view,
        name="send_friend_request"
    ),

    path(
        "friend-request/<int:request_id>/accept/",
        accept_friend_request_view,
        name="accept_friend_request"
    ),

    path(
        "friend-request/<int:request_id>/decline/",
        decline_friend_request_view,
        name="decline_friend_request"
    ),
    
    path(
        "friend/remove/<int:user_id>/",
        remove_friend_view,
        name="remove_friend"
    ),
    
    path(
    "community/cancel-request/<int:request_id>/",
        cancel_friend_request,
        name="cancel_friend_request"
    ),

    path(
        "notification/",
        notification_view,
        name="notifications"
    ),
    
    path(
    "notification/<int:notification_id>/",
    notification_redirect_view,
    name="notification_redirect"
),
]