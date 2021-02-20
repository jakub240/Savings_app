from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import Expense, AppUsers
from .forms import AddExpenseForm, AddUserForm, LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required


class LandingPageView(View):
    def get(self, request):
        return render(request,'base.html')


"""class PeriodsListView(View):
    def get(self, request):
        return render(request, 'periods.html')"""


"""class ExpenseListView(View):
    def get(self, request):
        return render(request, 'expense_list.html')"""


class ExpensesListFormView(LoginRequiredMixin, View):
    login_url = '/login/'

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


class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                msg = 'There is no such user!'
                return render(request, "login.html", {"form": form, 'msg': msg})
            else:
                login(request, user=user)
                return redirect('landing-page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing-page')


class AddUserView(FormView):
    form_class = AddUserForm
    template_name = "add_user.html"
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)

"""
class ChangePasswordView(FormView):
    form_class = UserPasswordChangeForm
    template_name = "change_password.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        id = self.kwargs["id"]
        user = User.objects.get(pk=id)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)
"""
