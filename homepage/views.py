from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import joblib
import pandas as pd
from collections import OrderedDict

model = joblib.load('./models/ModelForLoanRepayment.pkl')

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

@csrf_exempt
def predict(request):
    if request.method == 'POST':
       

        score = model.predict(pd.DataFrame({
            'Number of people who will provide maintenance' : request.POST.get('noofpeople'),
            'Loan History' : request.POST.get('loanhistory'),
            'Purpose of taking loan' : request.POST.get('purpose'),
            'loan amount taken' : request.POST.get('amt'),
            'Guarantor or Debtor' : request.POST.get('guarantorordebtor'),
            'Number of years of employment' : request.POST.get('empl'),
            'Marital Status' : request.POST.get('marital'),
            'Number of loans taken from current bank' : request.POST.get('loans'),
            'Age of the applicant in Number of Years' : request.POST.get('age'),
            'amount in current account' : request.POST.get('currentamt'),
            'amount in savings account' : request.POST.get('savingsamt'),
            '% of income paid as installment' : request.POST.get('percentofincome'),
            'Other loans plans taken' : request.POST.get('otherloanplans'),
            'Working abroad or not' : request.POST.get('workingabroad'),
            'Is there telephone number available' : request.POST.get('telephone'),
            'time duration for loan' : request.POST.get('timeduration'),
            'Owned property' : request.POST.get('ownedprop'),
            'Type of job performed' : request.POST.get('job'),
            'Type of Housing' : request.POST.get('housing'),
           'Number of years of stay in current address' : request.POST.get('noincurrentaddress'),
            }, index=[0]))

        if score==1:
            score = 0
        else:
            score = 1
    context = {'text' : score}
    return render(request, 'result.html', context)

