from rest_framework.serializers import ModelSerializer
from .models import Tags, Recipes


class TagsSerializer(ModelSerializer):
    model = Tags
    fields = ('id', 'name', 'color', 'slug')

class RecipesSerializer(ModelSerializer):
    model = Recipes
    fields = ('')