import random
import string

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User as BaseUser
# Create your models here.

# =====Base cloud models (@Tim Lauv)=============


class Product(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class AccountInfo(models.Model):
    '''Inherit within each product app'''
    name = models.CharField(max_length=32, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# =====Shared abstractral models (@Tim Lauv)=====


class Account(AccountInfo):
    '''Inherit within each product app, chicken'n'egg: you can have an account without primary_user at first'''
    info = models.OneToOneField(
        AccountInfo, parent_link=True, related_name='%(app_label)s_%(class)s', on_delete=models.CASCADE)
    primary_user = models.OneToOneField(
        'User', null=True, blank=True, related_name='no_reverse_+', on_delete=models.PROTECT)
    sso_account_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        if self.primary_user is not None:
            return str(self.primary_user.sso_login_id)
        else:
            return self.sso_account_id

    class Meta:
        abstract = True


class User(BaseUser):
    '''Inherit within each product app'''
    login = models.OneToOneField(
        BaseUser, parent_link=True, related_name='%(app_label)s_%(class)s', on_delete=models.PROTECT)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    sso_login_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return str(self.login)

    class Meta:
        abstract = True


class Device(models.Model):
    '''Inherit within each product app'''
    sn = models.CharField(max_length=16, primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    hwplatform = models.ForeignKey('HWPlatform', on_delete=models.PROTECT)
    group = models.ForeignKey('DeviceGroup', null=True, blank=True, on_delete=models.SET_NULL)
    profile = models.ForeignKey('Profile', null=True, blank=True, on_delete=models.PROTECT)
    firmware = models.ForeignKey('Firmware', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.sn

    class Meta:
        abstract = True


class HWPlatform(models.Model):
    '''Inherit within each product app'''
    SUPPORT_STATUS = (
        ('POC', 'POC'),
        ('REL', 'Release'),
        ('EOL', 'End of life'),
    )
    model = models.CharField(max_length=32, primary_key=True)
    support_status = models.CharField(max_length=3, choices=SUPPORT_STATUS)
    sn_prefix = models.CharField(max_length=6, validators=[MinLengthValidator(6)], unique=True)

    def __str__(self):
        return self.model

    class Meta:
        abstract = True


class Firmware(models.Model):
    '''Inherit within each product app'''
    version = models.CharField(max_length=32)
    hwplatform = models.ForeignKey('HWPlatform', on_delete=models.CASCADE)
    file = models.FileField(upload_to='firmwares/platform')

    def __str__(self):
        return self.hwplatform.model + "-" + self.version

    class Meta:
        abstract = True
        unique_together = ('version', 'hwplatform',)


class Profile(models.Model):
    '''Inherit within each product app'''
    name = models.CharField(max_length=128)  # short string (TBD:as short description?)
    config = models.TextField()  # single json block atm (TBD:pieces?)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DeviceGroup(models.Model):
    '''Inherit within each product app'''
    name = models.CharField(max_length=128)  # short string (TBD:as short description?)
    profile = models.ForeignKey('Profile', null=True, blank=True, on_delete=models.PROTECT)
    firmware = models.ForeignKey('Firmware', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# ===============================================


class CloudKey(models.Model):
    """
    |
    | mysql> select * from FortiCloudKeyView order by fortiCloudKeyTime desc limit 1;
    | +------------------+---------------+---------------------+
    | | serial           | fortiCloudKey | fortiCloudKeyTime   |
    | +------------------+---------------+---------------------+
    | | FG080D3914000688 | BCV8QATB      | 2017-01-10 15:30:06 |
    | +------------------+---------------+---------------------+
    |
    """
    sn = models.CharField(max_length=16, validators=[MinLengthValidator(16)], primary_key=True, db_column='serial')
    key = models.CharField(max_length=8, validators=[MinLengthValidator(8)], unique=True, db_column='fortiCloudKey')
    modified_at = models.DateTimeField(auto_now=True, db_column='fortiCloudKeyTime')

    def __init__(self, hwplatform_type, *args, **kwargs):
        super(CloudKey, self).__init__(*args, **kwargs)
        if not issubclass(hwplatform_type, HWPlatform):
            raise TypeError("Must pass a subclass of cloud.model.HWPlatform")
        self.__hwplatform_type = hwplatform_type

    def __str__(self):
        return self.sn + " - " + self.key

    @staticmethod
    def next_available_cloud_key(key_len=8):
        """
        Generate a key which does not exist in column CloudKey.fortiCloudKey

        :param key_len: optional key length parameter. By default it is 8.
        :return: a randomly generated key, which is composed by capital letters
                 and digits.
        """
        while True:
            key = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(key_len))
            try:
                CloudKey.objects.get(key=key)
            except ObjectDoesNotExist:
                break
        return key

    def clean(self):
        sn_prefix_col_name = 'sn_prefix'
        sn_prefix_set = {(lambda entry: entry[sn_prefix_col_name])(entry)
                         for entry in self.__hwplatform_type.objects.values(sn_prefix_col_name)}
        actual_sn_prefix = self.sn[0: 6]
        if actual_sn_prefix not in sn_prefix_set:
            raise ValidationError('\"%(actual_sn_prefix)s\" is not among hwplatform sn_prefix set.',
                                  params={'actual_sn_prefix': actual_sn_prefix})
            
class Question(models.Model):
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class People(models.Model):
    name=models.CharField(max_length=20)
    leader=models.ForeignKey('self',blank=True,null=True)

class Person(models.Model):
    friends = models.ManyToManyField("self")

class Publication(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)
    author = models.OneToOneField(People)

    def __str__(self):              # __unicode__ on Python 2
        return self.headline

    class Meta:
        ordering = ('headline',)


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the place" % self.name

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the restaurant" % self.place.name