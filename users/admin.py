from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    fields = ('image', 'phone', 'city', 'country', 'postcode')


class CustomUserAdmin(UserAdmin):
    model=User
    list_display=['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    search_fields = ('email', 'first_name', 'last_name')
    ordering=('email',)

    fieldsets=(
        (None, {'fields':('email','password')}),
        ('personal Info', {'fields':('first_name','last_name')}),
        ('Permissions', {'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
        ('Important Dates', {'fields':('last_login','date_joined')})
    )

    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2','is_staff','is_active')   
        }),
    )

    inlines = [ProfileInline]

    def get_inlines(self, request, obj=None):
        # Dynamically add inlines based on user type (if profile exists, etc.)
        return super().get_inlines(request, obj)

    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'postcode')
    list_filter = ('phone', 'city', 'country', 'postcode')
    search_fields = ('user__email', 'phone')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)