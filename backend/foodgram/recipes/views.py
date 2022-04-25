from django.db.models import BooleanField, Exists, OuterRef, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, Favorite, Recipe, Tag, Ingredient, IngredientAmount
from . import serializers, filters
from .permissions import AdminOrReadOnly, AdminUserOrReadOnly
from .paginations import LimitPageNumberPagination


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('^name',)
    filter_backends = (filters.IngredientSearchFilter,)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AdminUserOrReadOnly)
    pagination_classes = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipesReadSerializer
        return serializers.RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
    
    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    Favorite.objects.filter(
                        user=user,
                        recipe__pk=OuterRef('pk')
                    )
                ),
                is_in_shooping_cart=Exists(
                    Cart.objects.filter(
                        user=user,
                        recipe__pk=OuterRef('pk')
                    )
                )
            )
        else:
            queryset = queryset.annotate(
                is_favorited=Value(
                    False,
                    output_field=BooleanField()
                ),
                in_in_shopping_cart=Value(
                    False, output_field=BooleanField()
                )
            )

        return queryset

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        return self.add_object(Favorite, request.user, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.delete_object(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        return self.add_object(Cart, request.user, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.delete_object(Cart, request.user, pk)

    def add_object(self, model, user, pk):
        if model.objects.filter(
            user=user,
            recipe__id=pk,
        ).exists():
            return Response(
                {
                    'error': 'Возникла ошибка при добавлении рецепта',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(recipe=recipe, user=user)
        serializer = serializers.RecipesShortSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete_object(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                'error': 'Не получилось удалить рецепт'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        recipe = request.user.cart.all().value('recipe_id')
        ingredients = IngredientAmount.objects.filter(
            recipe__id__in=recipe
        )
        shopping_dict = {}
        for ingredient in ingredients:
            name = ingredient.ingredients.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredients.measurement_unit
            if name not in shopping_dict:
                shopping_dict[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                shopping_dict[name]['amount'] = (
                    shopping_dict[name]['amount'] + amount
                )

        shopping_list = []
        for index, key in enumerate(shopping_dict, start=1):
            shopping_list.append(
                f'{index}. {key} - {shopping_dict[key]["amount"]} '
                f'{shopping_dict[key]["measurement_unit"]}\n'
            )
        response = HttpResponse(
            shopping_list,
            content_type='text/plain',
        )
        response['Content-Disposition'] = ('attachment; '
                                           'filename=shopping_list.txt')
        return response
