from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Types(models.IntegerChoices):
        TRAINER = 1
        CUSTOMER = 2

    type = models.IntegerField(choices=Types.choices, default=Types.CUSTOMER)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=256, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class Trainer(Profile):
    experience = models.DecimalField(max_digits=2, decimal_places=0, default=0)


class Customer(Profile):
    historyOfBloodPressure = models.BooleanField(default=False, blank=True, null=True)
    historyOfDiabetes = models.BooleanField(default=False, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    days = models.PositiveSmallIntegerField(default=0)


class CustomerTrainer(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.trainer.user} trains {self.customer.user}'


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    relation = models.ForeignKey(CustomerTrainer, on_delete=models.CASCADE, blank=True, null=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)
    day = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    number = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
