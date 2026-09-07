from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import DiaryEntry, DiaryLike, DiaryComment, DiaryBookmark 
from community.models import Notification , FriendRequest
from .serializers import DiaryEntrySerializer
from accounts.models import User



# 1. CREATE A DIARY

@login_required
def diary_create_view(request):

    if request.method == "POST":

        serializer = DiaryEntrySerializer(
            data=request.POST
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return redirect("diary_list")

        return render(
            request,
            "diary_form.html",
            {
                "errors": serializer.errors,
                "data": request.POST
            }
        )

    return render(
        request,
        "diary/diary_form.html"
    )


# ==========================================
# 2. SHOW DIARIES
# ==========================================

@login_required
def diary_list_view(request):

    diaries = DiaryEntry.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for diary in diaries:
        
        diary.is_liked = diary.likes.filter(
            user=request.user
        ).exists()
        
        diary.is_bookmarked = diary.bookmarks.filter(
            user=request.user
        ).exists()

    return render(
        request,
        "diary_list.html",
        {
            "diaries": diaries
        }
    )


# ==========================================
# 3. EDIT A DIARY
# ==========================================

@login_required
def diary_edit_view(request, id):

    diary = get_object_or_404(
        DiaryEntry,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        serializer = DiaryEntrySerializer(
            diary,
            data=request.POST,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return redirect(
                "diary_detail",
                id=diary.id
            )

        return render(
            request,
            "diary/diary_edit.html",
            {
                "diary": diary,
                "errors": serializer.errors
            }
        )

    serializer = DiaryEntrySerializer(diary)

    return render(
        request,
        "diary/diary_edit.html",
        {
            "diary": serializer.data
        }
    )


# ==========================================
# 4. DELETE A DIARY
# ==========================================

@login_required
def diary_delete_view(request, id):

    diary = get_object_or_404(
        DiaryEntry,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        diary.delete()

        return redirect("diary_list")

    return render(
        request,
        "diary/diary_confirm_delete.html",
        {
            "diary": diary
        }
    )
    
    
@login_required
def diary_like_view(request, id):
    
    diary = get_object_or_404(
        DiaryEntry,
        id=id
    )
    
    if request.method == "POST":
        
        like, created = DiaryLike.objects.get_or_create(
            diary=diary,
            user=request.user  
        )
        
        # New like
        if created:
             
            # Don't notify when liking own diary              
            if diary.user != request.user:
                    
                Notification.objects.create(
                    recipient = diary.user,
                    sender = request.user,
                    notification_type = "like",
                    diary = diary
                )
                
        # Like already exists → remove it     
        else:
            like.delete()
                    
    return redirect(
        request.META.get("HTTP_REFERER", "home")
    )

@login_required
def diary_comment_view(request,id):
    
    diary = get_object_or_404(
        DiaryEntry,
        id=id
    )
    
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        
        if content:
            
            DiaryComment.objects.create(
                diary=diary,
                user=request.user,
                content=content
            )
            
            if diary.user != request.user:

                Notification.objects.create(
                    recipient=diary.user,
                    sender=request.user,
                    notification_type="comment",
                    diary=diary
                )
            
    return redirect(
        request.META.get("HTTP_REFERER", "home")
    )

# Save or remove user diary bookmark
@login_required
def diary_bookmark_view(request,id):
    
    diary = get_object_or_404(
        DiaryEntry,
        id = id,
    )
    
    if request.method == "POST":
    
        bookmark = DiaryBookmark.objects.filter(
            diary=diary,
            user=request.user
        ).first()
        

        if bookmark:
            # Already saved → remove bookmark
            bookmark.delete()
        else:
            # Not saved → create bookmark
            DiaryBookmark.objects.create(
                diary=diary,
                user=request.user
            )

    return redirect(
        request.META.get("HTTP_REFERER", "home")
    )
    
    
@login_required
def saved_diaries_view(request):

    saved_diaries = DiaryEntry.objects.filter(
        bookmarks__user=request.user
    ).order_by(
        "-bookmarks__created_at"
    )
    
    for diary in saved_diaries:

        diary.is_liked = diary.likes.filter(
            user=request.user
        ).exists()

    return render(
        request,
        "saved_diaries.html",
        {
            "saved_diaries": saved_diaries,
        }
    )

@login_required
def my_activity_view(request):

    # =====================================================
    # SUMMARY COUNTS
    # =====================================================

    diary_count = DiaryEntry.objects.filter(
        user=request.user
    ).count()

    like_count = DiaryLike.objects.filter(
        user=request.user
    ).count()

    comment_count = DiaryComment.objects.filter(
        user=request.user
    ).count()

    bookmark_count = DiaryBookmark.objects.filter(
        user=request.user
    ).count()


   
    # ACTIVITIES
    activities = []


    # DIARIES CREATED

    created_diaries = DiaryEntry.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for diary in created_diaries:

        activities.append({
            "type": "diary",
            "diary": diary,
            "created_at": diary.created_at,
        })


    # LIKES
    liked_diaries = DiaryLike.objects.filter(
        user=request.user
    ).select_related(
        "diary",
        "diary__user"
    ).order_by("-created_at")

    for like in liked_diaries:

        activities.append({
            "type": "like",
            "diary": like.diary,
            "created_at": like.created_at,
        })


    # -----------------------------------------------------
    # COMMENTS
    # -----------------------------------------------------

    commented_diaries = DiaryComment.objects.filter(
        user=request.user
    ).select_related(
        "diary",
        "diary__user"
    ).order_by("-created_at")

    for comment in commented_diaries:

        activities.append({
            "type": "comment",
            "diary": comment.diary,
            "created_at": comment.created_at,
        })


    # -----------------------------------------------------
    # BOOKMARKS
    # -----------------------------------------------------

    saved_diaries = DiaryBookmark.objects.filter(
        user=request.user
    ).select_related(
        "diary",
        "diary__user"
    ).order_by("-created_at")

    for bookmark in saved_diaries:

        activities.append({
            "type": "bookmark",
            "diary": bookmark.diary,
            "created_at": bookmark.created_at,
        })


    # =====================================================
    # FRIEND ACTIVITIES
    # =====================================================

    friend_activities = FriendRequest.objects.filter(
        Q(sender=request.user) |
        Q(receiver=request.user),
        status="accepted"
    ).select_related(
        "sender",
        "receiver"
    ).order_by("-created_at")


    for friend in friend_activities:

        activities.append({
            "type": "friend_accepted",
            "diary": None,
            "created_at": friend.created_at,
            "friend": (
                friend.receiver
                if friend.sender == request.user
                else friend.sender
            ),
        })


    # =====================================================
    # SORT ALL ACTIVITIES
    # =====================================================

    activities.sort(
        key=lambda activity: activity["created_at"],
        reverse=True
    )


    return render(
        request,
        "my_activity.html",
        {
            "activities": activities,

            "diary_count": diary_count,
            "like_count": like_count,
            "comment_count": comment_count,
            "bookmark_count": bookmark_count,
        }
    )
    
@login_required
def search_view(request):
    
    query = request.GET.get("q", "").strip()
    
    users = User.objects.none()
    diaries = DiaryEntry.objects.none()
    
    if query:
        
        #search people
        users = User.objects.filter(
            name__icontains=query
        ).exclude(
            id=request.user.id
        )
        
        # Search public diaries
        diaries = DiaryEntry.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query),
            visibility="public"
        ).select_related("user").order_by("-created_at")

    return render(
        request,
        "search.html",
        {
            "query": query,
            "users": users,
            "diaries": diaries
        }
    )