from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipesReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount')
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount')
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        for ingredient in ingredients:
            if isinstance(ingredient.get('amount'), str):
                if not ingredient.get('amount').isdigit():
                    raise serializers.ValidationError(
                        'Кол-во должно быть числом'
                    )
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    'Минимальное кол-во 1'
                )
            id_ingedient = ingredient.get('id')
            if id_ingedient in ingredients_set:
                raise serializers.ValidationError(
                    'Нельзя повторять ингридиент'
                )
            ingredients_set.add(id_ingedient)
        data['ingredients'] = ingredients
        return data

    def add_ingredients_tags(self, instance, **validated_data):
        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')
        for tag in tags:
            instance.tags.add(tag)

        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=instance,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_tags(
            recipe,
            tags=tags,
            ingredients=ingredients,
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        instance = self.add_ingredients_tags(
            instance,
            tags=tags,
            ingredients=ingredients,
        )
        return super().update(
            instance,
            validated_data,
        )
