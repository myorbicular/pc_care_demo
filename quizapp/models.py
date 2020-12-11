import datetime
from django.db import models
from django.utils import timezone
#from .result import oil_dry_anls
from django.core.exceptions import ObjectDoesNotExist


GENDER_CHOICES = [("1", "Male"), ("2", "Female"), ("3", "Others")]

AGE_CHOICES = (
    ("1", "18-25"),
    ("2", "26-35"),
    ("3", "36-45"),
    ("4", "46-55"),
    ("5", "55+"),
)


class Customer(models.Model):
    employee_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='1')
    age = models.CharField(max_length=1, choices=AGE_CHOICES, default='1')
    location = models.CharField(max_length=100)

    def __str__(self):
        # return self.name
        return f'{self.employee_id} - {self.name}'
    
    @property
    def get_oil_dry(self):
        '''it's return get_oil_dry'''
        oil_dry_ctx = None #oil_dry_anls(self.employee_id)
        return oil_dry_ctx
    
    @property
    def get_hydration(self):
        '''it's return get_oil_dry'''
        try:
            hydration = Hydration.objects.get(self.employee_id)
        except ObjectDoesNotExist:
            hydration = None
        return hydration


class PersonalCare(models.Model):
    code = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    personalcare = models.ForeignKey(PersonalCare, on_delete=models.CASCADE)
    code = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # code = models.CharField(null=True, blank=True, max_length=100)
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    marks = models.FloatField()

    def __str__(self):
        return self.name


class QuizModal(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    result = models.FloatField(default=0)

    def __str__(self):
        return str(self.choice)


class Hydration(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    weight = models.FloatField(default=0)
    physical_activity = models.FloatField(default=0)
    water_intake = models.FloatField(default=0)
    status = models.CharField(max_length=200)


class Concerns(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(Category, related_name='concerns')
    is_primary = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='is_primary')


class Products(models.Model):
    code = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    #content = models.TextField()
    cleanser = models.CharField(max_length=100)
    moisturizer = models.CharField(max_length=100)
    serum = models.CharField(max_length=100)

    def __str__(self):
        return self.title