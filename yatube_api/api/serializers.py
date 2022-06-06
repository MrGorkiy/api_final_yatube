from django.contrib.auth import get_user_model
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Follow
        fields = ("user", "following")
        read_only_fields = ("user",)

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("following", "user")
            )
        ]

    # def create(self, validated_data):
    #     following = self.initial_data.get('following')
    #     following = User.objects.get(username=following)
    #     user = validated_data.pop('user')
    #     print(following, user)
    #     if following != user:
    #         follow = Follow.objects.create(user=user, following=following)
    #         return follow

    def validate_following(self, value):
        print(value)
        following = User.objects.get(username=value)
        if not following:
            raise serializers.ValidationError("Пользователь не найден!")
        return value

    def validate(self, data):
        user = self.context["request"].user
        if user == data["following"]:
            raise serializers.ValidationError(
                "Нельзя подписаться самого на себя"
            )
        return data


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Post
        fields = ("id", "author", "text", "pub_date", "group", "image")
        read_only_fields = ("author",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("post",)


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created")
        read_only_fields = ("author", "post")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "slug", "title", "description")


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "slug", "title")
