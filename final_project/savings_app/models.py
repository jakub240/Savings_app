from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Cities(models.Model):
    """
    Model for cities:
    name = name of the city
    country = country
    region = administrative unit (state, land, province, voivodeship etc)
    key = special code
    """
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    key = models.IntegerField(default=00000)

    def __str__(self):
        return self.name


class AppUsers(AbstractUser):
    """
    This is an overwrite of auth.User model with two additional columns:
    date_of_birth = date of birth
    city = city of a user
    """
    date_of_birth = models.DateTimeField()
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)


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


class Budget(models.Model):
    """
        Model for maximum amount of expenses given by user to bear within selected period of time
          - start_date: beginning of a time period for which a budget is applied
          - end_date: end of a time period for which a budget is applied
          - amount: an equivalent of 'price' column in Expense model
          - category: relation to Category model
    """
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.FloatField(default=0)
    owner = models.ForeignKey(AppUsers, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)