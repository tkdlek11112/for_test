from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, nickname, phone, password=None):
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, nickname, phone, password):
        user = self.create_user(
            email,
            name=name,
            nickname=nickname,
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, null=False)
    nickname = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    gender = models.CharField(max_length=6, choices=(('male', '남자'), ('female', '여자')))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_order_num = models.CharField(max_length=12,null=True)
    last_product_name = models.CharField(max_length=100, null=True)
    last_order_date = models.DateTimeField(null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'users'
