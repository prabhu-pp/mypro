from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(unique=True, max_length=50)
    account_name = models.CharField(max_length=100)
    app_secret_token = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=10)
    headers = models.JSONField()