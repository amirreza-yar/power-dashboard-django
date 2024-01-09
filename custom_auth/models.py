from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    UUID_FIELD = 'uuid'
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)