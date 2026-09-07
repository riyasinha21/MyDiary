from django.db import models

from accounts.models import User, BaseModel


class DiaryEntry(BaseModel):
    
    PRIVATE = "private"
    PUBLIC = "public"
    
    VISIBILITY_CHOICES = (
        (PRIVATE, "Private"),
        (PUBLIC, "Public"),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="digital_entries"
    )
    
    title = models.CharField(max_length=255)
    
    content = models.TextField()
    
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default=PRIVATE
    )
    
    def __str__(self):
        return self.title

class DiaryLike(BaseModel):

    diary = models.ForeignKey(
        DiaryEntry,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diary", "user"],
                name="unique_diary_like"
            )
        ]

    def __str__(self):
        return f"{self.user.name} liked {self.diary.title}"
    
class DiaryComment(BaseModel):
    
    diary = models.ForeignKey(
        DiaryEntry,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    content = models.TextField()
    
    def __str__(self):
        return f"{self.user.name} commented on {self.diary.title}"
    
    
class DiaryBookmark(BaseModel):

    diary = models.ForeignKey(
        DiaryEntry,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmarked_diaries"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diary", "user"],
                name="unique_diary_bookmark"
            )
        ]

    def __str__(self):
        return f"{self.user.name} saved {self.diary.title}"