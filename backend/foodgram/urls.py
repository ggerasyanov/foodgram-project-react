from django.contrib import admin
from django.urls import include, path
from recipes import views as view_recipe
from rest_framework.routers import DefaultRouter

from users import views as view_user

router = DefaultRouter()

router.register('users', view_user.FollowViewSet)
router.register('tags', view_recipe.TagViewSet)
router.register('ingredients', view_recipe.IngredientViewSet)
router.register('recipes', view_recipe.RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
