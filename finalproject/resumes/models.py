from django.db import models

# Create your models here.
class Resume(models.Model):
    filename = models.IntegerField()
    title = models.CharField(max_length=255)
    resume_text = models.TextField()