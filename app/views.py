from django.views import View
from django.db.models import Case, When, Value, PositiveSmallIntegerField
from django.views.generic import ListView
from django.db.models import Q, Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CompanyForm, CompanySearchForm, PreferenceForm, CompanyNoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Company, Favorite, Preference, CompanyNote
from django.views.generic.edit import FormMixin, DeleteView, UpdateView
from django.urls import reverse_lazy
from .mixins import AdminRequiredMixin

# サインアップビュー
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

# ログアウトビュー
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('home')

# ホームページビュー
def home(request):
    return render(request, 'app/home.html')

# 会社追加ビュー
@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "会社が正常に追加されました。")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"エラーが発生しました: {e}")
        else:
            # バリデーションエラーを表示
            messages.error(request, "フォームにエラーがあります。")
            print(form.errors)  # エラー内容をコンソールに出力
    else:
        form = CompanyForm()

    # 選択肢の情報をコンテキストに追加
    context = {
        'form': form,
        'Engineering_Field_choices': Company.Engineering_Field.choices,
        'Programming_Language_choices': Company.Programming_Language.choices,
        'Training_choices': Company.Training.choices,
        'Growth_Environment_choices': Company.Growth_Environment.choices,
        'Ways_Of_Working_choices': Company.Ways_Of_Working.choices,
    }

    return render(request, 'app/add_company.html', context)
# お気に入り追加・削除ビュー
def add_favorite(request, company_id):
    if not request.user.is_authenticated:
        return redirect('login')  # ログインしていない場合はログインページにリダイレクト

    company = get_object_or_404(Company, pk=company_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, company=company)

    if not created:
        favorite.delete()  # すでにお気に入りに追加されていた場合は削除する（トグル機能）

    return redirect('company_detail', pk=company_id)  # 詳細ページにリダイレクト

# お気に入りトグルビュー
@login_required
def toggle_favorite(request, pk):
    company = get_object_or_404(Company, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, company=company)
    if not created:
        favorite.delete()
    return redirect('company_detail', pk=pk)

# 会社検索ビュー
def search_companies(request):
    form = CompanySearchForm(request.GET or None)
    query = form.cleaned_data.get('query', '') if form.is_valid() else ''
    
    # 初期のクエリセット（全ての会社を含む）
    companies = Company.objects.all()

    # デバッグ: クエリの値を確認
    print("Query:", query)

    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(working_hours__icontains=query) |
            Q(salary__icontains=query) |
            Q(preference__preference_level__icontains=query)
        ).distinct()

    # デバッグ: クエリセットの内容を確認
    print("Companies QuerySet:", companies)

    # ログインユーザーの志望選択を注釈に追加
    if request.user.is_authenticated:
        preferences = Preference.objects.filter(user=request.user).values('company_id', 'preference_level')

        preference_mapping = {
            pref['company_id']: pref['preference_level']
            for pref in preferences
        }

        companies = companies.annotate(
            preference_level=Case(
                *[
                    When(id=company_id, then=Value(level))
                    for company_id, level in preference_mapping.items()
                ],
                default=Value(None),
                output_field=IntegerField(),
            )
        )

    return render(request, 'app/search_companies.html', {'form': form, 'companies': companies, 'query': query})

def filter_companies(request):
    # フィルタ条件の取得
    employee_count_min = request.GET.get('employee_count_min', '')
    salary_min = request.GET.get('salary_min', '')  # 基本給以上
    salary_max = request.GET.get('salary_max', '')  # 基本給以下
    overtime_max = request.GET.get('overtime_max', '')  # 残業時間以下
    engineering_field = request.GET.get('engineering_field', '')
    programming_language = request.GET.get('programming_language', '')
    training = request.GET.get('training', '')
    growth_environment = request.GET.get('growth_environment', '')
    ways_of_working = request.GET.get('ways_of_working', '')

    # 初期クエリセット
    companies = Company.objects.all()

    # 数値フィルタリングの適用
    if employee_count_min:
        companies = companies.filter(employee_count__gte=int(employee_count_min))
    
    if salary_min:
        companies = companies.filter(salary__gte=int(salary_min))
    
    if salary_max:
        companies = companies.filter(salary__lte=int(salary_max))
    
    if overtime_max:
        companies = companies.filter(overtime__lte=int(overtime_max))
    
    # 文字列フィルタリングの適用
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
    
    # ユーザーの志望選択情報
    user_preferences = Preference.objects.filter(user=request.user)
    user_favorite = Favorite.objects.filter(user=request.user)
    
    # ユーザーごとの志望選択情報を辞書に格納
    user_preferences_dict = {pref.company_id: pref.preference_level for pref in user_preferences}

    # contextの準備
    context = {
        'companies': companies,
        'user_preferences': user_preferences_dict,
        'user_favorite': user_favorite,
        'Engineering_Field_choices': Company.Engineering_Field.choices,
        'Programming_Language_choices': Company.Programming_Language.choices,
        'Training_choices': Company.Training.choices,
        'Growth_Environment_choices': Company.Growth_Environment.choices,
        'Ways_Of_Working_choices': Company.Ways_Of_Working.choices,
    }
    
    return render(request, 'app/filter_companies.html', context)

# お気に入り一覧表示
def favorite_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favorites = Favorite.objects.filter(user=request.user).select_related('company')
    companies = [favorite.company for favorite in favorites]
    
    return render(request, 'app/favorite_list.html', {'companies': companies})

class CompanyListView(FormMixin, ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    form_class = CompanyForm
    success_url = reverse_lazy('company_list')

    def get_queryset(self):
        user = self.request.user
        preferences = Preference.objects.filter(user=user)
        queryset = Company.objects.all().annotate(
            preference_level=Case(
                *[
                    When(id=preference.company.id, then=Value(preference.preference_level))
                    for preference in preferences
                ],
                default=Value(None),
                output_field=PositiveSmallIntegerField(),
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Initialize the form
        return context

    def post(self, request, *args, **kwargs):
    # フォームの POST データを処理
        for key, value in request.POST.items():
            if key.startswith('name_'):
                # company_id をキーから抽出
                company_id = key.split('_')[1]
                # 対象の Company オブジェクトを取得
                company = get_object_or_404(Company, id=company_id)
                # Company の名前を更新
                company.name = value
                company.save()

                # チェックボックスに基づいて preference_level を設定
                preference_level = (
                    1 if request.POST.get(f'first_choice_{company_id}') else
                    2 if request.POST.get(f'second_choice_{company_id}') else
                    3 if request.POST.get(f'third_choice_{company_id}') else
                    4 if request.POST.get(f'fourth_choice_{company_id}') else
                    5 if request.POST.get(f'other_choice_{company_id}') else
                    None
                )

                # Preference オブジェクトを取得または作成
                preference, created = Preference.objects.get_or_create(user=request.user, company=company)
                if preference_level is not None:  # preference_level が None でないことを確認
                    preference.preference_level = preference_level
                    preference.save()
                else:
                    # preference_level が None の場合、Preference を削除するかどうかを判断
                    preference.delete()
                
                # 成功メッセージを表示
                messages.success(request, f"{company.name} の詳細が更新されました。")

        # 更新されたクエリセットでレスポンスを返す
        return self.get(request, *args, **kwargs)

# 志望選択肢更新ビュー
@login_required
def update_choices(request):
    if request.method == 'POST':
        # POST データの各項目を処理
        for key, value in request.POST.items():
            if key.startswith(('first_choice_', 'second_choice_', 'third_choice_')):
                # キーから choice_type と company_id を抽出
                choice_type, _, company_id = key.split('_')
                # 対象の Company オブジェクトを取得
                company = get_object_or_404(Company, id=company_id)
                # Company オブジェクトに choice_type 属性が存在するか確認
                if hasattr(company, choice_type):
                    # 属性の値を更新
                    setattr(company, choice_type, value == 'on')
                    company.save()
                else:
                    # 属性が存在しない場合の処理（必要に応じて）
                    pass
    # 'company_list' ビューにリダイレクト
    return redirect('company_list')
# 会社詳細ビュー
class CompanyDetailView(View):
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        is_favorite = Favorite.objects.filter(user=request.user, company=company).exists() if request.user.is_authenticated else False
        user_note = CompanyNote.objects.filter(user=request.user, company=company).first() if request.user.is_authenticated else None
        context = {
            'company': company,
            'is_favorite': is_favorite,
            'user_note': user_note,
        }
        return render(request, 'app/company_detail.html', context)

# 会社検索フォームビュー
def search_companies(request):
    form = CompanySearchForm(request.GET or None)
    companies = Company.objects.all()  # 初期状態で全ての会社を取得

    # フォームが有効な場合にフィルタリング
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            companies = companies.filter(
                Q(name__icontains=query) |
                Q(working_hours__icontains=query) |
                Q(salary__icontains=query) |
                Q(preference__preference_level__icontains=query)
            ).distinct()

    # 数値フィルタリングの適用
    employee_count_min = request.GET.get('employee_count_min', '')
    salary_min = request.GET.get('salary_min', '')
    salary_max = request.GET.get('salary_max', '')
    overtime_max = request.GET.get('overtime_max', '')

    if employee_count_min:
        companies = companies.filter(employee_count__gte=int(employee_count_min))

    if salary_min:
        companies = companies.filter(salary__gte=int(salary_min))

    if salary_max:
        companies = companies.filter(salary__lte=int(salary_max))

    if overtime_max:
        companies = companies.filter(overtime__lte=int(overtime_max))

    # 文字列フィルタリングの適用
    engineering_field = request.GET.get('engineering_field', '')
    programming_language = request.GET.get('programming_language', '')
    training = request.GET.get('training', '')
    growth_environment = request.GET.get('growth_environment', '')
    ways_of_working = request.GET.get('ways_of_working', '')

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

    # ユーザーの志望選択情報
    user_preferences = Preference.objects.filter(user=request.user) if request.user.is_authenticated else []
    user_favorite = Favorite.objects.filter(user=request.user) if request.user.is_authenticated else []

    # ユーザーごとの志望選択情報を辞書に格納
    user_preferences_dict = {pref.company_id: pref.preference_level for pref in user_preferences}

    # ユーザーのお気に入り情報をセット
    favorite_companies = {fav.company_id for fav in user_favorite}

    # コンテキストの準備
    context = {
        'form': form,
        'companies': companies,
        'user_preferences': user_preferences_dict,
        'favorite_companies': favorite_companies,
        'Engineering_Field_choices': Company.Engineering_Field.choices,
        'Programming_Language_choices': Company.Programming_Language.choices,
        'Training_choices': Company.Training.choices,
        'Growth_Environment_choices': Company.Growth_Environment.choices,
        'Ways_Of_Working_choices': Company.Ways_Of_Working.choices,
    }

    return render(request, 'app/search_companies.html', context)

# ユーザーの志望設定ビュー
@login_required
def set_preference(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = request.user
            preference.save()
            return redirect('some_view_name')  # ここにリダイレクト先のビュー名を指定
    else:
        form = PreferenceForm()
    
    return render(request, 'set_preference.html', {'form': form})

@login_required
def add_edit_note(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    note = CompanyNote.objects.filter(user=request.user, company=company).first()

    if request.method == 'POST':
        form = CompanyNoteForm(request.POST, instance=note)
        if form.is_valid():
            company_note = form.save(commit=False)
            company_note.user = request.user
            company_note.company = company
            company_note.save()
            messages.success(request, "メモが保存されました。")
            return redirect('company_detail', pk=company.id)
        else:
            messages.error(request, "メモの保存に失敗しました。")
    else:
        form = CompanyNoteForm(instance=note)

    return render(request, 'app/add_edit_note.html', {'form': form, 'company': company})

class CompanyDeleteView(AdminRequiredMixin, DeleteView):
    model = Company
    template_name = 'app/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdateView(AdminRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'app/company_form.html'
    success_url = reverse_lazy('company_list')  # 編集後にリダイレクトするURL

    def get_queryset(self):
        # adminユーザー専用でフィルタリングが必要な場合はこちらで実装
        return super().get_queryset()