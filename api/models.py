from django.db import models

STATUS_CHOICES = (
    ("collected", "collected"),
    ("in_progress", "in_progress"),
    ("active", "active"),
)


class Consumer(models.Model):
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    previous_jobs_count = models.IntegerField()
    amount_due = models.IntegerField()
    lat = models.DecimalField(max_digits=13, decimal_places=10)
    lng = models.DecimalField(max_digits=13, decimal_places=10)
