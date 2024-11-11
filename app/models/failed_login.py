from django.db import models


class Failed_Login(models.Model):
    FAILED_LOGIN_FROM_BACKEND = 'backend'
    FAILED_LOGIN_FROM_FRONTEND = 'frontend'
    FAILED_LOGIN_FROM = (
        ('backend', 'backend'),
        ('frontend', 'frontend'),
    )
    failed_login_id = models.AutoField('Id', primary_key=True)
    failed_login_username = models.CharField(
        'Username', max_length=255, blank=False)
    failed_login_password = models.CharField(
        'Password', max_length=255, blank=False)
    failed_login_from = models.CharField('From', max_length=20, choices=FAILED_LOGIN_FROM,
                                         default=FAILED_LOGIN_FROM_FRONTEND)
    failed_login_ip_address = models.CharField(
        "Ip Address", max_length=100, blank=False
    )
    failed_login_attempted_at = models.IntegerField(
        "Updated At", blank=False, default=0
    )
    failed_login_status = models.IntegerField("Status", blank=False, default=0)

    class Meta:
        db_table = "failed_login"
