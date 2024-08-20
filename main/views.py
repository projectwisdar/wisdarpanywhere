import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group  # Correct import for Group
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.utils import timezone
from django.conf import settings
from django.utils.translation import activate, get_language
from django.http import HttpResponse
from urllib.parse import urlparse
from django.contrib.admin.models import LogEntry
from django.db import transaction, IntegrityError

# Import your models
from .models import User, Task, Supervisor, MessageGroup, Message

from . import form_utilities, checks
from .checks import admin_check
from .form_utilities import *

# Import additional utilities or custom functions if needed
from django.utils.http import url_has_allowed_host_and_scheme
import logging
from .forms import TaskForm


User = get_user_model()

def set_language(request):
    next_url = request.POST.get('next', request.GET.get('next'))
    if not next_url or not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        next_url = request.META.get('HTTP_REFERER', '/')

    response = redirect(next_url)
    lang_code = request.POST.get('language', request.GET.get('language'))
    if lang_code and lang_code in dict(settings.LANGUAGES).keys():
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        activate(lang_code)

    # Debugging output
    print(f"Session language: {request.session.get('django_language')}")
    print(f"Cookie language: {request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)}")
    print(f"Current language: {get_language()}")

    return response


logger = logging.getLogger(__name__)

def login_user_from_form(request, body):
    logger.debug("login_user_from_form called with request method: %s, body: %s", request.method, body)
    
    if not isinstance(body, dict):
        logger.error("Expected 'body' to be a dictionary-like object, but got %s", type(body))
        raise ValueError("Expected 'body' to be a dictionary-like object")
    
    email = body.get("email")
    password = body.get("password")
    logger.debug("Extracted email: %s", email)
    
    if not all([email, password]):
        logger.warning("Email or password missing: email=%s", email)
        return None, "You must provide an email and password."
    
    email = email.lower()
    user = authenticate(username=email, password=password)
    remember = body.get("remember")
    logger.debug("Authenticated user: %s, remember: %s", user, remember)
    
    if user is None:
        logger.warning("Authentication failed for email: %s", email)
        return None, "Invalid email or password."
    
    login(request, user)
    logger.info("User %s logged in successfully", user)
    
    if remember is not None:
        request.session.set_expiry(0)  # Set session expiry if 'remember' is checked
        logger.debug("Session expiry set to 0 (until browser closes)")
    
    return user, None

def login_view(request):
    context = {'navbar': 'login'}
    logger.debug("login_view called with request method: %s", request.method)
    
    if request.method == 'POST':
        logger.debug("Handling POST request for login")
        user, message = login_user_from_form(request, request.POST)
        
        if user:
            logger.info("Login successful for user: %s", user)
            login(request, user)
            
            if user.is_superuser:
                logger.debug("User is superuser, redirecting to /logs/")
                return redirect('main:logs')
            else:
                logger.debug("User is not superuser, redirecting to main:logs")
                return redirect('main:my_tasks')
        
        elif message:
            logger.warning("Login failed with message: %s", message)
            context['error_message'] = message
    
    else:
        logger.debug("Rendering login page for GET request")
    
    return render(request, 'login.html', context)

def logout_view(request):
    """
    Logs the user out and redirects the user to the login page.
    :param request: The Django request.
    :return: A 301 redirect to the login page.
    """
    logout(request)
    return redirect('app:login')



def signup(request):
    context = full_signup_context(None)
    context['is_signup'] = True

    if request.method == 'POST':
        user, message = handle_user_form(request, request.POST)
        if user:
            login(request, user)  # Directly use Django's login function
            addition(request, user)
            return redirect('main:my_tasks')
        else:
            context['error_message'] = message

    context['navbar'] = 'signup'
    return render(request, 'signup.html', context)

def full_signup_context(user):
    """
    Returns a dictionary containing valid years, months, days, and groups in the database
    for the signup form.
    """
    return {
        "year_range": reversed(range(1900, datetime.date.today().year + 1)),  # Years from 1900 to the current year
        "day_range": range(1, 32),  # Days 1 to 31
        "months": [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ],
        "groups": Group.objects.all(),  # All groups in the database
    }




def handle_add_group_form(request, body):
        name = body.get('name')
        recipient_ids = body.getlist('recipient')
        message = body.get('message')

        if not all([name, recipient_ids, message]):
            return None, "All fields are required."
        if not [r for r in recipient_ids if r.isdigit()]:
            return None, "Invalid recipient."
        group = MessageGroup.objects.create(name=name)
        try:
            ids = [int(r) for r in recipient_ids]
            recipients = User.objects.filter(pk__in=ids)
        except User.DoesNotExist:
            return None, "Could not find user."
        group.members.add(request.user)
        group.members.add(*recipients)
        group.save()
        Message.objects.create(sender=request.user, body=message, group=group, date=timezone.now())
        return group, None
def handle_user_form(request, body, user=None):
    password = body.get("password")
    confirm_password = body.get("confirm_password")

    if password != confirm_password:
        return None, "Passwords do not match."

    try:
        # Ensure the 'Employee' group exists
        try:
            employee_group = Group.objects.get(name='Employee')
        except Group.DoesNotExist:
            employee_group = Group.objects.create(name='Employee')

        first_name = body.get("first_name")
        last_name = body.get("last_name")
        email = body.get("email").lower()
        phone = form_utilities.sanitize_phone(body.get("phone_number"))
        month = int(body.get("month"))
        day = int(body.get("day"))
        year = int(body.get("year"))
        date_of_birth = datetime.date(year, month, day)
        supervisor_id = body.get("supervisor")
        supervisor = Supervisor.objects.get(pk=int(supervisor_id)) if supervisor_id else None
        pic = request.FILES.get("thumbnail")

        if not all([first_name, last_name, email, phone, month, day, year]):
            return None, "All fields are required."

        if not form_utilities.email_is_valid(email):
            return None, "Invalid email."

        if user:
            # Update existing user
            user.email = email
            user.phone_number = phone
            user.first_name = first_name
            user.last_name = last_name
            user.date_of_birth = date_of_birth
            user.supervisor = supervisor

            if pic:
                user.thumbnail.save(pic.name, pic)

            user.save()

            if request.user.is_authenticated:
                change(request, user, 'User updated successfully.')
            
            return user, "User information updated successfully."
        else:
            # Check if a user with the given email already exists
            if get_user_model().objects.filter(email=email).exists():
                return None, "A user with that email already exists."

            # Create new user
            user = get_user_model().objects.create_user(
                username=email, email=email, password=password, first_name=first_name,
                last_name=last_name, date_of_birth=date_of_birth, phone_number=phone, supervisor=supervisor
            )

            if pic:
                user.thumbnail.save(pic.name, pic)

            # Add user to the 'Employee' group
            user.groups.add(employee_group)

            if request.user.is_authenticated:
                addition(request, user)

            return user, "User created successfully."

    except IntegrityError as e:
        logger.error(f"Integrity error during user creation: {e}")
        return None, "An error occurred while creating the user. Please try again."
    
#def check_email(request):
    return render(request, 'check_email.html')

@login_required
def my_tasks(request):
    return tasks(request, request.user.pk)


@login_required
def tasks(request, user_id):
    requested_user = get_object_or_404(User, pk=user_id)
    is_editing_own_tasks = requested_user == request.user
    if not is_editing_own_tasks and not request.user.has_perm('main.change_user', requested_user):
        raise PermissionDenied

    context = {}  # Populate context as necessary
    context['requested_user'] = requested_user
    context['user'] = request.user
    context['tasks'] = requested_user.tasks.all()  # Assuming tasks is a ManyToManyField

    if request.method == 'POST':
        task_form = TaskForm(request.POST)  # Example form for adding/editing tasks
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = requested_user
            task.save()
            requested_user.tasks.add(task)
            return redirect('main:tasks', user.pk)

    context['navbar'] = 'my_tasks' if is_editing_own_tasks else 'tasks'
    return render(request, 'tasks.html', context)

@login_required
def messages(request, error=None):
    recipients = User.objects.exclude(pk=request.user.pk)
    message_groups = request.user.messagegroup_set.annotate(max_date=Max('messages__date')).order_by('-max_date').all()
    
    for group in message_groups:
        group.has_unread = any(request.user not in message.read_members.all() for message in group.messages.all())
    
    context = {
        'navbar': 'messages',
        'user': request.user,
        'recipients': recipients,
        'groups': message_groups,
        'error_message': error
    }
    return render(request, 'messages.html', context)

def user_list_view(request):
    users = User.objects.all().order_by('-is_online', '-last_login_time')
    return render(request, 'user_table.html', {'users': users})


def home(request):
    return render(request, 'home.html')

def docs(request):
    return render(request, 'docs.html')


def user_list_view(request):
    # Order by is_online (True first), then by last_login_time (most recent first)
    users = User.objects.all().order_by('-is_online', '-last_login_time')
    return render(request, 'user_table.html', {'users': users})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:my_tasks')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def my_tasks(request):
    tasks = Task.objects.filter(user=request.user)  # Assuming there's a relation with the user
    return render(request, 'my_tasks.html', {'tasks': tasks})
    
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
@user_passes_test(checks.admin_check)
def logs(request):
    User = get_user_model()
    
    users = User.objects.all().order_by('-is_online', '-last_login_time')
    
    # Message and group statistics
    group_count = MessageGroup.objects.count()
    message_count = Message.objects.count()
    average_count = float(message_count) / float(group_count) if group_count > 0 and message_count > 0 else 0
        
    context = {
        "navbar": "logs",
        "user": request.user,
        "logs": LogEntry.objects.all().order_by('-action_time'),
        "users": users,  # Ensure users are passed here
        "stats": {
            "admin_count": User.objects.filter(is_superuser=True).count(),
            "conversation_count": group_count,
            "average_message_count": average_count,
            "message_count": message_count
        }
    }
    return render(request, 'logs.html', context)

