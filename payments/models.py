from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    devices = models.IntegerField()
    validity = models.CharField(max_length=50)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class MpesaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User is optional
    plan_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed")
        ],
        default="Pending"
    )
    checkout_request_id = models.CharField(max_length=100, null=True, blank=True)
    result_desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"{user_name} - {self.plan_name} - {self.status}"


    
