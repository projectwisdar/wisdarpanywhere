from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  # <-- Add this import

class Supervisor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()  # Link to the finished task or article
    date_completed = models.DateTimeField(default=timezone.now)  # <-- You are using timezone here

    def __str__(self):
        return self.title

class User(AbstractUser):
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=30)
    tasks = models.ManyToManyField(Task, blank=True)  # User's completed tasks
    supervisor = models.ForeignKey(Supervisor, null=True, on_delete=models.SET_NULL)
    thumbnail = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    is_online = models.BooleanField(default=False)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)



    REQUIRED_FIELDS = ['date_of_birth', 'phone_number', 'email', 'first_name', 'last_name']

    def unread_message_count(self):
        return Message.objects.filter(group__members__pk=self.pk).exclude(read_members__pk=self.pk).distinct().count()

class MessageGroup(models.Model):
    name = models.CharField(max_length=140)
    members = models.ManyToManyField(User)

    def latest_message(self):
        if this.messages.count() == 0:
            return None
        return self.messages.order_by('-date').first()

    def combined_names(self, full=False):
        names_count = self.members.count()
        extras = names_count - 3
        members = self.members.all()
        if not full:
            members = members[:3]
        names = ", ".join([m.get_full_name() for m in members])
        if extras > 0 and not full:
            names += " and %d other%s" % (extras, "" if extras == 1 else "s")
        return names

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    group = models.ForeignKey(MessageGroup, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField()
    read_members = models.ManyToManyField(User, related_name='read_messages')

    def preview_text(self):
        return (self.body[:100] + "...") if len(self.body) > 100 else self.body

