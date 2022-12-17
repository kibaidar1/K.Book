from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Book, Page, User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    search_fields = ['username']

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class PageInline(admin.TabularInline):
    model = Page

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
        ('Author', {'fields': ('author',)}),
        ('In favorites', {'fields': ('users', )})
    )
    list_display = ('name', 'slug', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at', 'updated_at')
    inlines = [PageInline]
    search_fields = ('author__username', 'name', 'created_at', 'pages__content')

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
# admin.site.register(Page, PageAdmin)
