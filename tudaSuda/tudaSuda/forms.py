from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label_suffix=False, label='', max_length=50,
                            widget=forms.EmailInput(attrs={'placeholder': 'Почта',
                                                           'autocomplete': "off"}))
    password = forms.CharField(label_suffix=False, label='', max_length=50,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                            'autocomplete': "off"}))
class RegistrationForm(forms.Form):
    name = forms.CharField(label_suffix=False, label='', max_length=20, min_length=4,
                           widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                        'autocomplete': "off"}))
    email = forms.CharField(label_suffix=False, label='', max_length=50,
                            widget=forms.EmailInput(attrs={'placeholder': 'Почта',
                                                        'autocomplete': "off"}))
    password = forms.CharField(label_suffix=False, label='', max_length=50,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                            'autocomplete': "off"}))
    password1 = forms.CharField(label_suffix=False, label='', max_length=50,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль',
                                                            'autocomplete': "off"}))
