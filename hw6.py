from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    is_subscribed = models.BooleanField(default=False)

from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

from django.shortcuts import render
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from .models import User

def subscribe(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.POST['user_id'])
        user.is_subscribed = True
        user.save()
        return redirect('main')

<form action="{% url 'subscribe' %}" method="post">
    {% csrf_token %}
    <input type="hidden" name="user_id" value="{{ user.id }}">
    <button type="submit">Подписаться</button>
</form>

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", hours=24)
def send_newsletter():

    subscribers = User.objects.filter(is_subscribed=True)

    for subscriber in subscribers:
        send_email(subscriber.email, "Текст рассылки")


from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):

        scheduler.start()