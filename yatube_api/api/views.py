from posts.models import Comment, Follow, Group, Post, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import (
    CommentDetailSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupListSerializer,
    GroupSerializer,
    PostSerializer,
)


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(
                MultiSerializerViewSetMixin, self
            ).get_serializer_class()


class PostViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """Получить список всех публикаций. При указании параметров limit и offset
    выдача должна работать с пагинацией."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    serializer_action_classes = {
        "comments": CommentSerializer,
        "detail_comments": CommentDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == "retrieve":
            return (ReadOnly(),)
        return super().get_permissions()

    @action(
        detail=True,
        url_path="comments",
        methods=["get", "post"],
        permission_classes=(OwnerOrReadOnly,),
    )
    def comments(self, request, pk=None):
        if request.method == "GET":
            posts = Comment.objects.filter(post=pk)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                posts = Post.objects.get(pk=pk)
                serializer.save(author=self.request.user, post=posts)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=["get", "put", "patch", "delete"],
        url_path=r"comments/(?P<comment_id>\d+)",
        url_name="comment-post",
        permission_classes=(OwnerOrReadOnly,),
    )
    def detail_comments(self, request, pk, comment_id):
        if request.method == "GET":
            posts = Comment.objects.filter(post=pk).get(pk=comment_id)
            serializer = self.get_serializer(posts)
            return Response(serializer.data)
        elif request.method == "PUT":
            posts = Comment.objects.filter(post=pk).get(pk=comment_id)
            serializer = self.get_serializer(posts, data=request.data)
            if serializer.instance.author != self.request.user:
                raise PermissionDenied("Изменение чужого контента запрещено!")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == "PATCH":
            posts = Comment.objects.filter(post=pk).get(pk=comment_id)
            serializer = self.get_serializer(posts, data=request.data)
            if serializer.instance.author != self.request.user:
                raise PermissionDenied("Изменение чужого контента запрещено!")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == "DELETE":
            posts = Comment.objects.filter(post=pk).get(pk=comment_id)
            serializer = self.get_serializer(posts, data=request.data)
            if serializer.instance.author != self.request.user:
                raise PermissionDenied("Изменение чужого контента запрещено!")
            posts.delete()
            return Response(
                {"message": f"Комментарий id:{comment_id} удален"},
                status=status.HTTP_204_NO_CONTENT,
            )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        search = self.request.query_params.get("search")
        if search:
            search = User.objects.get(username=search).id
        if search is not None:
            queryset = queryset.filter(following=search)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return GroupListSerializer
        return GroupSerializer
