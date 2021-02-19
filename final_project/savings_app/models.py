from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

CITIES = (
    (1, 'Warszawa'),
    (2, 'Kraków'),
    (3, 'Gdańsk'),
    (4, 'Lublin'),
    (5, 'Kielce'),
    (6, 'Wrocław'),
    (7, 'Poznań'),
)


class AppUsers(AbstractUser):
    date_of_birth = models.DateTimeField()
    city = models.CharField(max_length=30, choices=CITIES)


class Category(models.Model):
    """
      - name: name of the category,
      - description: description of the category,
      - expenses - 'many to many' relation to User model through Expenses
      """
    name = models.CharField(max_length=60)
    description = models.TextField()
    expenses = models.ManyToManyField(AppUsers, through='Expense')

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
      - name: name of the expense,
      - description: description of the expense,
      - category: relation to the Category model,
      - owner: relation to the User model,
      - price: price of the expense,
      - created: date, when the expense was added
      """
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(AppUsers, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)


