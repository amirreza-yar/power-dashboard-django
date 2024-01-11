from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import base64

class CustomUser(AbstractUser):
    UUID_FIELD = 'uuid'
    
    uuid = models.CharField(max_length=22, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('utf-8')[:8]
        super().save(*args, **kwargs)