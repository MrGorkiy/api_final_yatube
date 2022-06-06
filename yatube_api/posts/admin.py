from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "image",
        "group",
        "pub_date",
        "author",
    )
    search_fields = (
        "text",
        "author",
        "group",
    )
    list_editable = ("group",)
    list_filter = (
        "pub_date",
        "group",
    )
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "post",
        "created",
    )
    search_fields = (
        "text",
        "author",
        "post",
    )
    list_filter = (
        "created",
        "author",
    )


@admin.register(Follow)
class FollowersAdmin(admin.ModelAdmin):
    list_display = (
        "following",
        "user",
    )
    search_fields = (
        "following",
        "user",
    )
    list_filter = (
        "following",
        "user",
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "slug",
    )
    search_fields = ("pk", "title", "slug")
    list_filter = (
        "title",
        "slug",
    )
