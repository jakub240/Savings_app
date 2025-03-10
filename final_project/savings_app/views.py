from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Expense, Budget, Category
from .forms import AddExpenseForm, AddUserForm, AddBudgetForm
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.core.paginator import Paginator


class LandingPageView(View):
    """
    Landing Page/Main Page.
    Renders base html
    """
    def get(self, request):
        return render(request, 'base.html')


class ExpensesListFormView(LoginRequiredMixin, View):
    """
    Main view for an app, available for logged User.
    Renders a list of Expenses and Budgets added by a User and offers a variety of calculations on these objects.
    It also includes an AddExpenseForm.
    """
    login_url = '/accounts/login/'

    def get(self, request):
        global bdg_days
        form = AddExpenseForm()
        expenses = Expense.objects.filter(owner=request.user).order_by('-expense_date')
        budgets = Budget.objects.filter(owner=request.user)

        categories = Category.objects.filter(owners=request.user)
        context_data_lst = []

        paginator = Paginator(expenses, 5)
        page = request.GET.get('page')
        expenses_in_pages = paginator.get_page(page)
        # ctx['expenses_in_pages'] = expenses_in_pages

        ctx = {'form': form,
               'expenses': expenses,
               'budgets': budgets,                
               'categories': categories,
               'expenses_in_pages': expenses_in_pages
        }

        if expenses:
            exp_sum = round(expenses.aggregate(Sum('price'))['price__sum'], 2)
            ctx['exp_sum'] = exp_sum            


        if budgets and expenses:            
            bdg_sum = round(budgets.aggregate(Sum('amount'))['amount__sum'], 2)            
            ctx['bdg_sum'] = bdg_sum  

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
                                                         expense_date__range=(bdg.start_date, bdg.end_date),
                                                         )
                else:
                    exp_per_ctg = []

                if exp_per_ctg:
                    exp_per_ctg_sum = round(exp_per_ctg.aggregate(Sum('price'))['price__sum'], 2)
                else:
                    exp_per_ctg_sum = 0

                if bdg_days <= 0:
                    bdg_per_day = 'Budget has come to an end'
                else:
                    bdg_per_day = str(round((bdg_per_ctg_sum - exp_per_ctg_sum) / bdg_days, 2))

                context_data_lst.append((ctg, exp_per_ctg_sum, bdg_days, bdg_per_day))

        ctx['ctx_lst'] = context_data_lst

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
                expense_date =form.cleaned_data['expense_date'],
                owner=current_user,
            )
        return redirect('expense-list-form')


class AddBudgetFormView(View):
    """
    A form view for adding object in Budget model
    """
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
    """
    Delete method for Expense model
    """
    def get(self, request, expense_id):
        Expense.objects.get(pk=expense_id).delete()
        return redirect('expense-list-form')


class BudgetRemoveView(View):
    """
    Delete method for Budget model
    """
    def get(self, request, budget_id):
        Budget.objects.get(pk=budget_id).delete()
        return redirect('expense-list-form')


class ExpenseModifyView(UpdateView):
    """
    Update method for Expense model
    """
    model = Expense
    fields = ['name', 'description', 'category', 'price', 'expense_date']
    template_name_suffix = '_modify'
    success_url = reverse_lazy('expense-list-form')


class BudgetModifyView(UpdateView):
    """
    Update method for Budget model
    """
    model = Budget
    fields = ['amount', 'category', 'start_date', 'end_date']
    template_name_suffix = '_modify'
    success_url = reverse_lazy('expense-list-form')


class AddUserView(FormView):
    """
    View for AddUserForm
    """
    form_class = AddUserForm
    template_name = "registration/add_user.html"
    success_url = reverse_lazy('landing-page')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class UserProfileView(View):
    """
    View displayed after successful login
    """
    def get(self, request):
        return render(request, 'registration/profile.html')




