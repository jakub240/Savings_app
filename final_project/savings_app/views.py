from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Expense, Budget, Category
from .forms import AddExpenseForm, AddUserForm, AddBudgetForm
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class LandingPageView(View):
    def get(self, request):
        return render(request, 'base.html')


class ExpensesListFormView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = AddExpenseForm()
        expenses = Expense.objects.filter(owner=request.user).order_by('-created')
        budgets = Budget.objects.filter(owner=request.user)
        exp_sum = expenses.aggregate(Sum('price'))['price__sum']
        bdg_sum = budgets.aggregate(Sum('amount'))['amount__sum']

        categories = Category.objects.filter(owners=request.user)
        budgets_lst = []

        ctx = {'form': form,
               'expenses': expenses,
               'budgets': budgets,
               'exp_sum': exp_sum,
               'bdg_sum': bdg_sum,
               'categories': categories,
               }

        if budgets or expenses:
            for ctg in categories:
                bdg_per_ctg_qs = Budget.objects.filter(owner=request.user, category=ctg.pk)
                bdg_per_ctg_sum = bdg_per_ctg_qs.aggregate(Sum('amount'))['amount__sum']

                if bdg_per_ctg_qs:
                    bdg = bdg_per_ctg_qs.first()
                    today = datetime.now().date()
                    if bdg.start_date <= today:
                        bdg_days = (bdg.end_date - today).days
                    else:
                        bdg_days = (bdg.end_date - bdg.start_date).days

                    exp_per_ctg = Expense.objects.filter(owner=request.user,
                                                         category=ctg.pk,
                                                         created__gte=bdg.start_date,
                                                         created__lte=bdg.end_date,
                                                         )
                else:
                    exp_per_ctg = []

                if exp_per_ctg:
                    exp_per_ctg_sum = exp_per_ctg.aggregate(Sum('price'))['price__sum']
                else:
                    exp_per_ctg_sum = 0

                bdg_per_day = str(round((bdg_per_ctg_sum - exp_per_ctg_sum) / bdg_days, 2))

                budgets_lst.append((ctg, bdg_per_ctg_sum, bdg_days, bdg_per_day))

        ctx['budgets_lst'] = budgets_lst

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
            )
        return redirect('expense-list-form')


class AddBudgetFormView(View):
    def get(self, request):
        form = AddBudgetForm()
        ctx = {
            'form': form
        }
        return render(request, 'add_budget_form.html', ctx)

    def post(self, request):
        form = AddBudgetForm(request.POST)
        current_user = request.user
        if form.is_valid():
            Budget.objects.create(
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                amount=form.cleaned_data['amount'],
                category=form.cleaned_data['category'],
                owner=current_user
            )
        return redirect('expense-list-form')


class ExpenseRemoveView(View):
    def get(self, request, expense_id):
        Expense.objects.get(pk=expense_id).delete()
        return redirect('expense-list-form')


class BudgetRemoveView(View):
    def get(self, request, budget_id):
        Budget.objects.get(pk=budget_id).delete()
        return redirect('expense-list-form')


class ExpenseModifyView(UpdateView):
    model = Expense
    fields = ['name', 'description', 'category', 'price']
    template_name_suffix = '_modify'
    success_url = reverse_lazy('expense-list-form')


class BudgetModifyView(UpdateView):
    model = Budget
    fields = ['amount', 'category', 'start_date', 'end_date']
    template_name_suffix = '_modify'
    success_url = reverse_lazy('expense-list-form')


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




