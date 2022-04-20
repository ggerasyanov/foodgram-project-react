# from django.db import models

# from ..users.models import User


# class Amount(models.Model):
#     amount = models.IntegerField(
#         verbose_name='Количество'
#     )


# class Ingredients(models.Model):
#     name = models.CharField(
#         verbose_name='Название'
#     )
#     measurement_unit = models.CharField(
#         verbose_name='Единица измерения'
#     )


# class Tags(models.Model):
#     name = models.CharField(
#         verbose_name='Название',
#         unique=True
#     )

#     slug = models.SlugField(
#         verbose_name='Жетон',
#         unique=True
#     )

#     color = models.CharField(
#         verbose_name='Цвет',
#         max_length=7,
#         unique=True
#     )


# class Recipes(models.Model):
#     author = models.ForeignKey(
#         User,
#         verbose_name='Автор',
#         on_delete=models.CASCADE,
#         related_name='user'
#     )

#     name = models.CharField(
#         verbose_name='Название рецепта',
#         max_length=56,
#         unique=True
#     )

#     image = models.ImageField(
#         verbose_name='Картинка',
#     )

#     text = models.TextField(
#         verbose_name='Описание',
#     )

#     ingredients = models.ManyToManyField(
#         IngredientAmount,
#         verbose_name='Ингридиенты',
#         on_delete=models.PROTECT,
#         related_name='ingredients',
#         limit_choices_to=True,
#     )

#     tags = models.ManyToManyField(
#         Tags,
#         verbose_name='Тег',
#         on_delete=models.PROTECT,
#         related_name='tags',
#         limit_choices_to=True
#     )

#     cooking_time = models.IntegerField(
#         max_length=3
#     )


# class IngredientAmount(models.Model):
#     recipes = models.ForeignKey(
#         Recipes,
#         verbose_name='Рецепт',
#         on_delete=models.CASCADE
#     )

#     ingredient = models.ForeignKey(
#         Ingredients,
#         verbose_name='Ингридиенты',
#         on_delete=models.PROTECT
#     )

#     amount = models.ForeignKey(
#         Amount,
#         verbose_name='Количество',
#         on_delete=models.PROTECT
#     )
