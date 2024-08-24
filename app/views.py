from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CompanyForm
from .models import Company

def home(request):
    return render(request, 'app/home.html')

#会社追加
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        print("------------------------------------")
        print("フォームのデータ:", request.POST)
        print("====================================")
        print("フォームエラー:", form.errors)
        print("------------------------------------")
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except Exception as e:
                # Print the specific error to the console
                print(f"Error saving company: {e}")
                form.add_error(None, "エラーが発生しました。もう一度お試しください。")
        else:
            # Print form errors for debugging
            print("Form is not valid:", form.errors)
    else:
        form = CompanyForm()

    context = {
        'form': form,
        'Engineering_Field_choices': Company.Engineering_Field.choices,
        'Programming_Language_choices': Company.Programming_Language.choices,
        'Training_choices': Company.Training.choices,
        'Growth_Environment_choices': Company.Growth_Environment.choices,
        'Ways_Of_Working_choices': Company.Ways_Of_Working.choices,
    }

    return render(request, 'app/add_company.html', context)

#検索機能
def search_company(request):
    query = request.GET.get('q', '')
    companies = Company.objects.filter(name__icontains=query)
    return render(request, 'app/search_company.html', {'companies': companies, 'query': query})

#フィルター機能
def filter_companies(request):
    employee_count = request.GET.get('employee_count', '')
    overtime = request.GET.get('overtime', '')
    salary = request.GET.get('salary', '')
    engineering_field = request.GET.get('engineering_field', '')
    programming_language = request.GET.get('programming_language', '')
    training = request.GET.get('training', '')
    growth_environment = request.GET.get('growth_environment', '')
    ways_of_working = request.GET.get('ways_of_working', '')

    companies = Company.objects.all()
    
    if employee_count:
        companies = companies.filter(employee_count=employee_count)
    if overtime:
        companies = companies.filter(overtime=overtime)
    if salary:
        companies = companies.filter(salary=salary)
    if engineering_field:
        companies = companies.filter(engineering_field=engineering_field)
    if programming_language:
        companies = companies.filter(programming_language=programming_language)
    if training:
        companies = companies.filter(training=training)
    if growth_environment:
        companies = companies.filter(growth_environment=growth_environment)
    if ways_of_working:
        companies = companies.filter(ways_of_working=ways_of_working)
    
    context = {
        'companies': companies,
        'Engineering_Field_choices': Company.Engineering_Field.choices,
        'Programming_Language_choices': Company.Programming_Language.choices,
        'Training_choices': Company.Training.choices,
        'Growth_Environment_choices': Company.Growth_Environment.choices,
        'Ways_Of_Working_choices': Company.Ways_Of_Working.choices,
        'selected_engineering_field': engineering_field,
        'selected_programming_language': programming_language,
        'selected_training': training,
        'selected_growth_environment': growth_environment,
        'selected_ways_of_working': ways_of_working,
    }
    return render(request, 'app/filter_companies.html', context)

#第一志望、第二志望、第三志望機能
def view_choices(request):
    first_choice_companies = Company.objects.filter(first_choice=True)
    second_choice_companies = Company.objects.filter(second_choice=True)
    third_choice_companies = Company.objects.filter(third_choice=True)
    
    return render(request, 'app/view_choices.html', {
        'first_choice_companies': first_choice_companies,
        'second_choice_companies': second_choice_companies,
        'third_choice_companies': third_choice_companies,
    })

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'app/company_list.html', {'companies': companies})

def update_choices(request):
    if request.method == 'POST':
        for company_id in request.POST:
            if company_id.startswith('first_choice_'):
                company = Company.objects.get(id=company_id.split('_')[2])
                company.first_choice = request.POST.get(company_id) == 'on'
                company.save()
            elif company_id.startswith('second_choice_'):
                company = Company.objects.get(id=company_id.split('_')[2])
                company.second_choice = request.POST.get(company_id) == 'on'
                company.save()
            elif company_id.startswith('third_choice_'):
                company = Company.objects.get(id=company_id.split('_')[2])
                company.third_choice = request.POST.get(company_id) == 'on'
                company.save()
    return redirect('company_list')

class CompanyDetailView(View):
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        return render(request, 'app/company_detail.html', {'company': company})