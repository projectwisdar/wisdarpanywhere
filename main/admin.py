from django.contrib import admin
from .models import User, Supervisor, Task, MessageGroup, Message
from django.contrib.auth.admin import UserAdmin

# Register the User model with the custom UserAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'phone_number', 'tasks', 'supervisor', 'thumbnail', 'is_online', 'last_login_time', 'last_logout_time')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_online', 'last_login_time', 'last_logout_time')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Register the Supervisor model
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')

# Register the Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'date_completed')
    search_fields = ('title',)
    list_filter = ('date_completed',)

# Register the MessageGroup model
class MessageGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('members',)  # For ManyToManyField

# Register the Message model
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'date')
    search_fields = ('sender__username', 'body')
    list_filter = ('date',)
    filter_horizontal = ('read_members',)  # For ManyToManyField

# Register all models with their respective admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(MessageGroup, MessageGroupAdmin)
admin.site.register(Message, MessageAdmin)
