from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import Expense, AppUsers
from .forms import AddExpenseForm, AddUserForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required


class LandingPageView(View):
    def get(self, request):
        return render(request, 'base.html')


"""class PeriodsListView(View):
    def get(self, request):
        return render(request, 'periods.html')"""


"""class ExpenseListView(View):
    def get(self, request):
        return render(request, 'expense_list.html')"""


class ExpensesListFormView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = AddExpenseForm()
        expense_list = Expense.objects.all()
        ctx = {
            'expense_list': expense_list,
            'form': form
        }
        return render(request, 'add_expense_form.html', ctx)

    def post(self, request):
        form = AddExpenseForm(request.POST)
        current_user = request.user
        if form.is_valid():
            Expense.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                price=form.cleaned_data['price'],
                owner=current_user,
                created=datetime.now()
            )

        return redirect('expense-list-form')


class AddUserView(FormView):
    form_class = AddUserForm
    template_name = "registration/add_user.html"
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class UserProfileView(View):
    def get(self, request):
        return render(request, 'registration/profile.html')


# class LogoutView(View):
#     def get(self, request):
#         return render(request, 'registration/logout.html')

