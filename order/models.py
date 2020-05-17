from django.db import models

# Create your models here.


class Order(models.Model):
    order_num = models.CharField(unique=True, max_length=12)
    product_name = models.CharField(max_length=100, null=False, default='제품명')
    order_date = models.DateTimeField()
    email = models.EmailField(verbose_name='email', max_length=100)

    class Meta:
        db_table = 'order'