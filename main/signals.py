from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .models import User

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f"User {user.username} logged in at {now()}")  # Debugging statement
    user.is_online = True
    user.last_login_time = now()
    user.save()
    print(f"User {user.username} is_online: {user.is_online}, last_login_time: {user.last_login_time}")  # Debugging statement

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    print(f"User {user.username} logged out at {now()}")  # Debugging statement
    user.is_online = False
    user.save()
    print(f"User {user.username} is_online: {user.is_online}")  # Debugging statement