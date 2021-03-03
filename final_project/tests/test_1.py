import pytest
from django.test import Client
from savings_app.models import Expense, Budget, Category, AppUsers, Cities
from django.shortcuts import reverse
from datetime import datetime
from django.contrib.auth import get_user_model


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def city():
    city = Cities.objects.create(name='NightCity', country='Cyberpunk', region='dystopian', key=101010)
    return city


@pytest.fixture
def user(city):
    user = AppUsers.objects.create(
        username='test_user',
        password='test_password',
        date_of_birth='2000-01-01 00:00Z',
        city=city
    )
    return user


@pytest.fixture
def category():
    category = Category.objects.create(
        name='test_expense',
        description='test_desc',
    )
    return category


@pytest.fixture
def expense():
    expense = Expense.objects.create(
        name='test_expense',
        description='test_desc',
        category=category,
        owner=user,
        price=100,
    )
    return expense


@pytest.fixture
def budget():
    budget = Budget.objects.create(
        start_date='2000-01-01',
        end_date='2000-01-02',
        amount=1000,
        owner=user,
        category=category,
    )
    return budget


def test_landing_page(client):
    """
    tests the Landing_Page_View
    """
    response = client.get('')
    assert response.status_code == 200


def test_login_get(client):
    """
        tests Login View
    """
    response = client.get('/accounts/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(client):
    """
        tests using Post method on login form
    """
    response = client.post('/accounts/login/', {'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 200


def test_expense_view_not_logged(client):
    """
        tests and attempt to access Expense_List_Form_View while not logged in,
        by design it redirects to Login View
    """
    response = client.get('/expenses/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_expense_view_logged(client, user):
    """
            tests and attempt to access Expense_List_Form_View while logged in
    """
    client.force_login(user=user)
    response = client.get('/expenses/')
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_expenses_list_form_view(client):
#     client.force_login(user='test_user')
#     context = {
#         "name": 'test_expense',
#         "description": 'test_description',
#         'category': 'food',
#         "price": 19.99,
#         'owner': client,
#         'created': datetime.now(),
#
#     }
#     count = Expense.objects.count()
#     response = client.post(reverse('expenses'), context)
#     exp = Expense.objects.get(
#                             name='test_product',
#                             description='test_description',
#                             category='food',
#                             price=19.99,
#                             owner=client,
#                             created=datetime.now
#     )
#     assert exp != None
#     assert Expense.objects.count() == count + 1
#     assert response.status_code == 302


@pytest.mark.django_db
def test_add_budget_form(client, user, category):
    client.force_login(user=user)
    context = {
        'start_date': '2000-01-01',
        'end_date': '2000-01-02',
        'amount': 1000,
        'category': category,
        'owner': user,
    }
    count = Budget.objects.count()
    response = client.post(reverse('add-budget'), context)
    bdg = Budget.objects.get(
        start_date='2000-01-01',
        end_date='2000-01-02',
        amount=1000,
        category=category,
        owner=user,
    )
    assert bdg is not None
    assert Budget.objects.count() == count + 1
    assert response.status_code == 302
