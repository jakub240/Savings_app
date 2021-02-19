from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import Expense
from .forms import AddExpenseForm, AddUserForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

class LandingPageView(View):
    def get(self, request):
        return render(request,'base.html')


"""class PeriodsListView(View):
    def get(self, request):
        return render(request, 'periods.html')"""


"""class ExpenseListView(View):
    def get(self, request):
        return render(request, 'expense_list.html')"""


class ExpensesListFormView(View):
    def get(self, request):
        form = AddExpenseForm()
        expense_list = Expense.objects.all()
        for exp in expense_list:
            name = exp.name
            price = exp.price
            user = exp.owner
            date = exp.created
        ctx = {
            'expense_list': expense_list,
            'form': form
        }
        return render(request, 'add_expense_form.html', ctx)
    def post(self, request):
        pass


"""class LoginFormView(View):
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
                return render(request, "login.html", {"form": form})
            else:
                login(request, user=user)
                return redirect("index")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
"""

class AddUserView(FormView):
    form_class = AddUserForm
    template_name = "add_user.html"
    success_url = reverse_lazy("index")

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
        return super().form_valid(form)"""

