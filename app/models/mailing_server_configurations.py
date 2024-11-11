
from django.db import models

class MailServerConfig(models.Model):
    id = models.AutoField("Id", primary_key=True)
    host = models.CharField("Host", max_length=191)
    port = models.IntegerField("Port")
    username = models.CharField("User Name",max_length=191)
    password = models.CharField("Password",max_length=191)
    sender = models.CharField("Sender",max_length=191,default="")
    subject_prefix = models.CharField("Subject Prefix",max_length=191,default="")
    tls_enabled = models.BooleanField("TLS",default=True)
    ssl_enabled = models.BooleanField("SSL",default=False)

    created_at = models.IntegerField("Created At", blank=False, default=0)
    created_by = models.IntegerField("Created By", blank=False, default=0)
    updated_at = models.IntegerField("Updated At", blank=False, default=0)
    updated_by = models.IntegerField("Updated By", blank=False, default=0)