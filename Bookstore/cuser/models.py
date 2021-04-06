from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.conf import settings
from django.shortcuts import reverse

from allauth.socialaccount.signals import pre_social_login, social_account_added, social_account_updated
from allauth.account.signals import user_signed_up
from storages.backends.s3boto3 import S3Boto3Storage

class UserManager(BaseUserManager):
    def create_user(self, email, password, full_name, **extra_fields):
        """
        Create and save a User with the given email, fullname, and password.
        """
        if not email:
            raise ValueError(_('The user must have an email'))

        if not password:
            raise ValueError(_('The user must have a password'))

        if not full_name:
            raise ValueError(_('The user must have a full name'))

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password, full_name, **extra_fields):
        """
        Create and save a SuperUser with the given email, fullname, and password.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, full_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    # is_superuser field provided by PermissionsMixin if we use PermissionsMixin
    # groups field provided by PermissionsMixin if we use PermissionsMixin
    # user_permissions field provided by PermissionsMixin if we use PermissionsMixin

    full_name = models.CharField(max_length=255, unique=False, blank=False, null=False, verbose_name=_('full name'))
    email = models.EmailField(_('email'), max_length=255, unique=True, blank=False, null=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_('phone number'), blank=True, null= True, max_length=17, validators=[phone_regex])
    
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=7, blank=True, null=True, choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    img = models.ImageField(blank=True, null=True, verbose_name='Image')
    email_verified = models.BooleanField(verbose_name='Email Verified', default=False)
    # phone_verified = models.BooleanField(verbose_name='Phone Verified')
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]   # while creating superuser from command it will ask these fields to enter value.
    EMAIL_FIELD = 'email'              # this is returned when we call get_email_field_name() method.


    class Meta:
        ordering = ['-email',]


    def __str__(self):
        email = '%s' % (self.email)
        return email

    def get_full_name(self):
        return self.full_name.strip()

    def get_short_name(self):
        return self.full_name.split(' ')[0]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm_list, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self):pass

    def get_user_permissions(self):pass

    def get_group_permissions(self):pass

    def get_all_permissions(self):pass



@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin.account.provider == 'google':
        # print('########### Inside user_signed_up signal handler function###########')
        # print('sociallogin: ', sociallogin)
        # print('user: ', user)
        # print('user data: ', user.socialaccount_set.filter(provider='google')[0].extra_data )
        # print('####################################################################')
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data          
        user.full_name = user_data['given_name']
        user.email_verified = True
        user.save()

    # if sociallogin.account.provider == 'facebook':
    #     user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    #     picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"            
    #     email = user_data['email']
    #     first_name = user_data['first_name']

    # if sociallogin.account.provider == 'linkedin':
    #     user_data = user.socialaccount_set.filter(provider='linkedin')[0].extra_data        
    #     picture_url = user_data['picture-urls']['picture-url']
    #     email = user_data['email-address']
    #     first_name = user_data['first-name']

    # if sociallogin.account.provider == 'twitter':
    #     user_data = user.socialaccount_set.filter(provider='twitter')[0].extra_data
    #     picture_url = user_data['profile_image_url']
    #     picture_url = picture_url.rsplit("_", 1)[0] + "." + picture_url.rsplit(".", 1)[1]
    #     email = user_data['email']
    #     first_name = user_data['name'].split()[0]

    # user.profile.avatar_url = picture_url
    # user.profile.email_address = email
    # user.profile.first_name = first_name
    # user.profile.save()  


# allauth.Socialaccount signals are not working.
# user_model = get_user_model()

# def social_account_setup(request, user, **kwargs):
#     print('########### Inside  social_account_added signal handler function###########')
#     print('request: ', request)
#     print('user: ', user)
#     print('####################################################################')

# social_account_added.connect(social_account_setup, sender=user_model)


