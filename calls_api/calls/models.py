from django.db import models

recording_choices = (
    ('START', 'Start'),
    ('END', 'End')
)

class CallRecord(models.Model):
    type = models.CharField('Type', max_length=10, choices=recording_choices)
    date_register = models.DateTimeField('Time register')
    call_id = models.CharField('Call', max_length=5)
    source = models.CharField('Origin phone number', max_length=12)
    destination = models.CharField('Destination phone number', max_length=12)
