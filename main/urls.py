from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-language/', views.set_language, name='set_language'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    
   # path('check-email/', views.check_email, name='check_email'),
    path('add-group/', views.handle_add_group_form, name='add_group'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('tasks/<int:user_id>/', views.tasks, name='tasks'),
    path('messages/', views.messages, name='messages'),
    path('user-list/', views.user_list_view, name='user_list'),
    path('user-table/', views.user_list_view, name='user_table'),
    path('create-task/', views.create_task, name='create_task'),
    path('profile/', views.profile, name='profile'),
    path('logs/', views.logs, name='logs'),
    path('docs/', views.docs, name='docs'),




]

