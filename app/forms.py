from django import forms
from .models import Company, Preference, CompanyNote, PlaceOfWork

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'  # モデルの全フィールドをフォームに含める
        widgets = {
            'first_choice': forms.CheckboxInput(),  # 'first_choice' フィールドにチェックボックスウィジェットを使用
            'second_choice': forms.CheckboxInput(),  # 'second_choice' フィールドにチェックボックスウィジェットを使用
            'third_choice': forms.CheckboxInput(),   # 'third_choice' フィールドにチェックボックスウィジェットを使用
            'place_of_work': forms.CheckboxSelectMultiple(),  # 複数選択可能なウィジェットを使用
        }

    # PlaceOfWorkの選択肢を提供するために、`form`の`__init__`メソッドをオーバーライドします
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place_of_work'].queryset = PlaceOfWork.objects.all()  # 選択肢として全`PlaceOfWork`オブジェクトを設定

        
class CompanySearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='検索')

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['company', 'preference_level']

class CompanyNoteForm(forms.ModelForm):
    class Meta:
        model = CompanyNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4}),
        }
    # モデルに選択肢が正しく定義されていれば、以下の再定義は不要です。
    # engineering_field = forms.ChoiceField(choices=Company.Engineering_Field.choices, required=False)
    # programming_language = forms.ChoiceField(choices=Company.Programming_Language.choices, required=False)
    # training = forms.ChoiceField(choices=Company.Training.choices, required=False)
    # growth_environment = forms.ChoiceField(choices=Company.Growth_Environment.choices, required=False)
    # ways_of_working = forms.ChoiceField(choices=Company.Ways_Of_Working.choices, required=False)
