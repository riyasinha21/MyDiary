from django.urls import path

from .views import (
    diary_create_view,
    diary_list_view,
    diary_edit_view,
    diary_delete_view,
    diary_like_view,
    diary_comment_view,
    diary_bookmark_view,
    saved_diaries_view,
    my_activity_view,
    search_view
)

urlpatterns = [

    path(
        "",
        diary_list_view,
        name="diary_list"
    ),

    path(
        "create/",
        diary_create_view,
        name="diary_create"
    ),

    path(
        "edit/<int:id>/",
        diary_edit_view,
        name="diary_edit"
    ),

    path(
        "delete/<int:id>/",
        diary_delete_view,
        name="diary_delete"
    ),
    
    path(
        "like/<int:id>/",
        diary_like_view,
        name="diary_like"
    ),
    
    path(
        "comment/<int:id>/",
        diary_comment_view,
        name="diary_comment"
    ),
    
    path(
        "diary/<int:id>/",
        diary_bookmark_view,
        name="diary_bookmark"
    ),
    
    path(
        "saved/",
        saved_diaries_view,
        name="saved_diaries"
    ),
    
    path(
        "activity/",
        my_activity_view,
        name="my_activity"
    ),
    
    
    path(
        "search/",
        search_view,
        name="search"
    ),
    
]