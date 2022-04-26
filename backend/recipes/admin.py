from django.contrib.admin import ModelAdmin, TabularInline, register

from users.models import Follow

from . import models as recipe_model


class IngredientInline(TabularInline):
    model = recipe_model.Recipe.ingredients.through


@register(recipe_model.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


@register(recipe_model.Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@register(recipe_model.Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Число добавлений в избранное'


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('user', 'author')
    autocomplete_fields = ('author', 'user')
    search_fields = ('user', 'author',)


@register(recipe_model.IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount',)
    search_fields = ('ingredients',)


@register(recipe_model.Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


@register(recipe_model.Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
