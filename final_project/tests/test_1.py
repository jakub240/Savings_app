import pytest
from django.test import Client
from savings_app.models import Expense, Budget, Category
from django.shortcuts import reverse
from datetime import datetime

@pytest.fixture
def client():
    client = Client()
    return client

def test_landing_page(client):
    response = client.get('')
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
def test_add_budget_form(client):
    client.force_login(user='test_user')
    context = {
        'start_date': '2000-12-01',
        'end_date': '2000-12-31',
        'amount': 1000,
        'category': 1,
        'owner': client.id,
    }
    count = Budget.objects.count()
    response = client.post(reverse('add-budget'), context)
    bdg = Budget.objects.get(
                        start_date='2000-12-01',
                        end_date='2000-12-31',
                        amount=1000,
                        category=1,
                        owner=client.id,
    )
    assert bdg != None
    assert Budget.objects.count() == count + 1
    assert response.status_code == 302