from django.db import models
from django.conf import settings

from accounts.models import  BaseModel


class FriendRequest(BaseModel):

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_friend_request"
            )
        ]

    def __str__(self):
        return f"{self.sender.name} → {self.receiver.name}"
    
    
#For notification
class Notification(BaseModel):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=[
            ("like", "Like"),
            ("comment", "Comment"),
            ("friend_request", "Friend Request"),
            ("friend_accepted","Friend Request Accepted"),
            ("new_post", "New Diary Post"),
        ]
    )

    diary = models.ForeignKey(
        "diary.DiaryEntry",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.sender.name} → {self.recipient.name} ({self.notification_type})"
