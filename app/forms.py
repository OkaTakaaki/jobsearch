from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'first_choice': forms.CheckboxInput(),
            'second_choice': forms.CheckboxInput(),
            'third_choice': forms.CheckboxInput(),
        }
        

    # モデルに選択肢が正しく定義されていれば、以下の再定義は不要です。
    # engineering_field = forms.ChoiceField(choices=Company.Engineering_Field.choices, required=False)
    # programming_language = forms.ChoiceField(choices=Company.Programming_Language.choices, required=False)
    # training = forms.ChoiceField(choices=Company.Training.choices, required=False)
    # growth_environment = forms.ChoiceField(choices=Company.Growth_Environment.choices, required=False)
    # ways_of_working = forms.ChoiceField(choices=Company.Ways_Of_Working.choices, required=False)
