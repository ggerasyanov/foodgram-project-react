from django.core import validators
from django.db import models

from users.models import User


class Tag(models.Model):

    name = models.CharField(
        max_length=200, verbose_name='Название', unique=True
    )

    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        unique=True,
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name='Slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )

    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        blank=True,
        verbose_name='Автор',
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )

    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='Картинка',
    )

    text = models.TextField(
        verbose_name='Описание',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )

    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Минимальное время приготовления одна минута'
        ),
        ]
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ('pub_date', )

    def __str__(self):
        return self.name


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_user'
            )
        ]

    def __str__(self):
        return f'Избранные {self.user} - {self.recipe}'


class IngredientAmount(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='В рецепте',
        related_name='ingredient',
    )

    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Связанные ингредиенты',
        related_name='recipe',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[validators.MinValueValidator(
            1, message='Минимальное кол-во ингридиентов - 1'
        ),
        ],
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Кол-во ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique_ingredients_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredients.name} - {self.amount}'


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart'
            )
        ]

    def __str__(self):
        return f'Корзина {self.user} - {self.recipe}'
