import pytest
from django.test import Client, TestCase
from savings_app.models import Expense, Budget, Category, AppUsers, Cities
from django.urls import reverse



@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def city():
    city = Cities.objects.create(
        name='NightCity',
        country='Cyberpunk',
        region='dystopian',
        key=101010)
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
        name='test_category',
        description='test_desc',
    )
    return category


@pytest.fixture
def expense(user, category):
    expense = Expense.objects.create(
        name='test_expense',
        description='test_desc',
        category=category,
        owner=user,
        price=100,
    )
    return expense


@pytest.fixture
def budget(user, category):
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


@pytest.mark.django_db
def test_add_user(user, client, city):
    """
        tests using Post method on AddUserView
    """
    response = client.get(reverse('add-user'))
    assert response.status_code == 200

    post_data = {'username': 'test_name2',
                 'first_name': 'test_first_name2',
                 'last_name': 'test_last_name2',
                 'password': 'test_password2',
                 'repeat_password': 'test_password2',
                 'email': 'test@mail.com',
                 'date_of_birth': '2000-01-01 00:00Z',
                 'city': city.pk
                 }
    count = AppUsers.objects.count()
    assert count == 1
    response = client.post(reverse('add-user'),post_data)

    assert AppUsers.objects.count() == count + 1
    assert response.status_code == 302


def test_expense_view_not_logged(client):
    """
        tests and attempt to access Expense_List_Form_View while not logged in,
        by design it redirects to Login View
    """
    response = client.get('/expenses/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_expense_view_logged(client, user, expense):
    """
            tests and attempt to access Expense_List_Form_View while logged in
            and getting an Expense and Budget objects
    """
    client.force_login(user=user)
    response = client.get(reverse('expense-list-form'))
    assert response.status_code == 200
    assert response.context['expenses'][0] == expense
    # assert response.context['budgets'][0] == budget


@pytest.mark.django_db
def test_expense_modify_get(client, user, expense):
    """
        test for ExpenseModifyView
    """
    client.force_login(user=user)
    response = client.get(reverse('expense-modify', kwargs={'pk': expense.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_budget_modify_get(client, user, budget):
    """
        test for BudgetModifyView
    """
    client.force_login(user=user)
    response = client.get(reverse('budget-modify', kwargs={'pk': budget.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_expenses_add(client, user, category, expense):
    """
        test for post method for ExpensesListFormView
    """
    client.force_login(user=user)
    post_data = {
        "name": 'test_expense',
        "description": 'test_description',
        'category': category.pk,
        "price": 100,

    }
    count = Expense.objects.count()
    response = client.post(reverse('expense-list-form'), post_data)

    assert Expense.objects.count() == count + 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_budget_add(budget, client, user, category):
    """
        test for AddBudgetFormView
    """
    client.force_login(user=user)
    post_data = {
        'start_date': '2000-01-15',
        'end_date': '2000-01-16',
        'amount': 2000,
        'category': category.pk,

    }
    count = Budget.objects.count()
    assert count == 1
    response = client.post(reverse('add-budget'), post_data)

    assert Budget.objects.count() == count + 1
    assert response.status_code == 302


