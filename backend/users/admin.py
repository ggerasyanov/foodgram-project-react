from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class AlterUserAdmin(UserAdmin):
    """Класс для удобной работы в админке. Изменяет вид отображения
    комментариев. Добавляет поиск и возможность сортировки
    для модели Follow."""
    list_display = ('username', 'email', 'password', 'first_name',
                    'last_name',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email', )
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, AlterUserAdmin)
