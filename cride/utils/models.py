
from django.db import models

class CSharingModel(models.Model):
    """Base model to add some extra data to models"""

    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Creation date'
    )

    modified = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text='Modified date'
    )

    class Meta:

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
