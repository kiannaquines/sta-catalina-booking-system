from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import *


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Username"}),
    )
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_type'].choices = [
            choice for choice in self.fields['user_type'].choices
            if choice[0] in ["Driver", "Regular User", "Manager"]
        ]

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"rows": 1, "class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

        self.fields['user_type'].label = "What are you?"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['address'].label = "Address"
        self.fields['is_member'].label = "Are you a member in COOP?"

    class Meta:
        model = CustomUserModel
        fields = [
            "first_name", 
            "last_name",
            "user_type",
            "phone_number",
            "address",
            "is_member",
        ]




class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': 'Email'})

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            else:
                field.widget.attrs.update({"class": "form-control"})
    
    class Meta:
        model = CustomUserModel
        
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = CustomUserModel
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "is_superuser",
            "is_active",
            "is_staff",
            "is_member",
        ]


class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = CustomUserModel
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "is_superuser",
            "is_active",
            "is_staff",
            "is_member",
        ]


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_delivered"].label = "Delivery Status"
        self.fields['date_reserved'].label = 'Date'
        if 'location' in self.fields:
            self.fields['location'].widget.attrs['readonly'] = True

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ReservationModel
        fields = [
            "reserved_by",
            "product_name",
            "quantity",
            "location",
            "truck",
            "date_reserved",
            "reservation_type",
            "is_delivered",
        ]
        widgets = {
            "date_reserved": forms.DateInput(
                attrs={"type": "text", "placeholder": "MM/DD/YYYY"}
            ),
            'location': forms.TextInput(attrs={'readonly':'readonly'})
        }
        


class TruckForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_reserved"].label = "Reserved"
        self.fields["is_available"].label = "Available"

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = TruckModel
        fields = "__all__"
