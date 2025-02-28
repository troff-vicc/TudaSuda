from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label_suffix=False, label='', max_length=50,
                            widget=forms.EmailInput(attrs={'placeholder': 'Имя',
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


class AddForm(forms.Form):
    boolFields = ((0, 'Нет'), (1, 'Да'))
    #images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    name = forms.CharField(label_suffix=False, label='', max_length=50,
                            widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                                           'autocomplete': "off"}))
    description = forms.CharField(label_suffix=False, label='', max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Описание',
                                                            'autocomplete': "off"}))
    private = forms.ChoiceField(label_suffix=False, label='', choices=boolFields)
    
    GPX = forms.CharField(label_suffix=False, label='', max_length=1000)
    

class EditForm(forms.Form):
    email = forms.CharField(label_suffix=False, label='', max_length=50,
                           widget=forms.EmailInput(attrs={'placeholder': 'Почта',
                                                          'autocomplete': "off"}))
    description = forms.CharField(label_suffix=False, label='', max_length=50,
                              widget=forms.TextInput(attrs={'placeholder': 'Описание',
                                                                'autocomplete': "off"}))
    img_file = forms.ImageField(label_suffix=False,label='', max_length=255)
    def __init__(self, *args, **kwargs):
        t = False
        if kwargs:
            t = True
            my_arg = kwargs.pop('my_arg')
        super(EditForm, self).__init__(*args, **kwargs)
        if t:
            self.initial['email'] = my_arg[1]
            self.initial['description'] = my_arg[0]
            