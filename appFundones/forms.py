from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder
from .secret import API_EMAIL_VALIDATION
import requests

class RegisterForm(forms.ModelForm):
    
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email ou celular'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar senha'})
    )
    class Meta:
        model = CustomUser
        fields = ('identifier', 'name', 'last_name', 'bday', 'gender', 'password', 'confirm_password')
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome', 'required': 'True'}), 
            'bday': forms.TextInput(attrs={'id': 'mask-bday','placeholder': 'Data de nascimento', 'required': 'True'}), 
            #'bday': forms.DateInput(attrs={'class': 'bday-form', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'gender'}),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Senha',
                'required': 'True'})
        }
       
    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.data.get("confirm_password")
        identifier = self.cleaned_data.get("identifier")
    
        if len(password) < 8:
            raise forms.ValidationError("Senha muito curta.")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")
        
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("A  senha deve conter pelo menos uma letra.")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        
        if not any(char.islower() for char in password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        
        if not any(char in '!@#$%^&*()_+-=[]{}|;\':",.<>?/~`' for char in password):
            raise forms.ValidationError("A senha deve conter pelo menos um caracter especial.")
        
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("Senhas não coincidem.")
        return password
        
        
    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier") 
        
        if "@" in identifier:
            if CustomUser.objects.filter(email=identifier):
                raise forms.ValidationError("Email já cadastrado.") 
            url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_EMAIL_VALIDATION}&email={identifier}"
            response = requests.get(url)
            response_data = response.json()
            print(url)
            if not response_data.get("deliverability") == "DELIVERABLE":
                raise forms.ValidationError("Entre com um email válido.")
            
        else:
            if CustomUser.objects.filter(phone_number=identifier):
                raise forms.ValidationError("Celular já cadastrado.")
                
            if not identifier.isdigit():
                raise forms.ValidationError("Entre com um email ou celular válido.")
            
        
            number_with_plus = '+' + identifier
            try:
                phonenumbers.parse(number_with_plus)
            except Exception:
                raise forms.ValidationError("Entre com um número de celular válido.")
                
                
        return identifier
    
    def save(self, commit=True):
        user = super().save(commit=False)
        identifier = self.cleaned_data.get('identifier')
        bday = self.cleaned_data.get('bday')
        format_date = datetime.strptime(bday, '%d/%m/%Y').strftime('%Y-%m-%d')
        user.bday = format_date
        print("aqui")
        if '@' in identifier:
            user.email = identifier
        else:
            user.phone_number = identifier
            number_with_plus = "+" + identifier
            number = phonenumbers.parse(number_with_plus)
            country = geocoder.country_name_for_number(number, 'pt')
            user.country = country
            
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            
        return user
            

class LoginForm(forms.Form):
    
    identifier = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Email ou celular'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": 'Senha'}))
    
    
    def clean(self):
        cleaned_data = super().clean()
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')
        
        if identifier and password:
            if '@' in identifier:
                user = authenticate(email=identifier, password=password)
                
            else:
                user = authenticate(phone_number=identifier, password=password)
            
            if not user:
                raise forms.ValidationError("usuário ou senha incorretos.")
            cleaned_data['user'] = user
        return cleaned_data
            

        
        
    

