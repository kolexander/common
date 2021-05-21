from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    """
        This model contains account info.
        Required:
            - disabled
            - created_at
            - updated_at
            - primary_email
            - disabled
            - last_name
    """

    disabled = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    primary_email = models.TextField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)


class SocialAccount(models.Model):
    """
        Social account model
    """

    class SocialType(models.IntegerChoices):
        LINKEDIN = 1
        FACEBOOK = 2
        GOOGLE = 3

    social_id = models.CharField(max_length=150)
    account = models.ForeignKey(
        Account, verbose_name='social_account',
        null=False, on_delete=models.CASCADE
    )
    social_type = models.IntegerField(choices=SocialType.choices)

    class Meta:
        db_table = 'social_account'
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'


def get_password_reset_token_expiry_time():
    """
    Returns the password reset token expiry time in hours (default: 24)
    """
    # get token validation time
    return getattr(settings, 'RESET_PASSWORD_EXPIRY', 24)


class User(models.Model):
    """
        This model contains users info.
        Required:
            - created_at
            - area
            - account
            - language
    """

    # 0 - applicant
    # 1 - employer
    created_at = models.DateTimeField()
    area = models.ForeignKey('grc_common.Area', on_delete=models.CASCADE)
    description = models.TextField(null=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
