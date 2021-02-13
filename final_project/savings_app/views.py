from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

# Create your views here.

class LandingPageView(View):
    def get(self, request):
        return render(request,'base.html')


class PeriodsListView(View):
    def get(self, request):
        return render(request, 'periods.html')


class ExpenseListView(View):
    def get(self, request):
        return render(request, 'expense-list.html')