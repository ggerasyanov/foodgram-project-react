from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Класс для удобной работы в админке. Изменяет вид отображения
    комментариев. Добавляет поиск и возможность сортировки
    для модели Follow."""
    list_display = ('username', 'email', 'password', 'first_name',
                    'last_name',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email', )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
