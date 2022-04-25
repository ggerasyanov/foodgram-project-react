from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from requests import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.models import Follow, User

from .serializers import FollowSerializer


class FollowViewSet(UserViewSet):

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={
                'request': request,
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        follow = Follow.objects.filter(author=author, user=user)

        if user == author:
            return Response(
                {
                    'error': 'Нельзя подписаться на себя',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if follow.exists():
            return Response(
                {
                    'error': 'Вы уже подписаны на автора'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow = Follow.objects.create(
            author=author,
            user=user,
        )
        serializer = FollowSerializer(
            follow,
            context={
                'request': request
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        follow = Follow.objects.filter(author=author, user=user)

        if not follow.exists():
            return Response(
                {
                    'error': 'Вы уже отписаны от автора',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
