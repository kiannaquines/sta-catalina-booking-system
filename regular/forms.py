from app.models import ReservationModel, ReservationProduct
from django import forms


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['date_reserved'].label = 'Date Reservation'
        self.fields['location'].widget.attrs.update({'readonly': True, 'class': 'form-control'})
        
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"rows": 3, "class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ReservationModel
        fields = '__all__'
        exclude = ['reserved_by', 'reservation_status', 'is_delivered', 'truck', 'is_cancelled']
        widgets = {
            'date_reserved': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_reservation': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'complete_address': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class ReservationProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].label = 'Product'
        self.fields['quantity'].label = 'Quantity'
        self.fields['delivery_quantity_type'].label = 'Type'

        self.fields['product_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['delivery_quantity_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ReservationProduct
        fields = '__all__'
        exclude = ['tied_with_reservation_of',]



class UpdateReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateReservationForm, self).__init__(*args, **kwargs)
        self.fields['date_reserved'].label = 'Date Reservation'
        self.fields['location'].widget.attrs.update({'readonly': True, 'class': 'form-control'})
        
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"rows": 3, "class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ReservationModel
        fields = '__all__'
        exclude = ['reserved_by', 'reservation_status', 'is_delivered', 'truck', 'is_cancelled']
        widgets = {
            'date_reserved': forms.TimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_reservation': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'complete_address': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class UpdateReservationProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateReservationProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].label = 'Product'
        self.fields['quantity'].label = 'Quantity'
        self.fields['delivery_quantity_type'].label = 'Type'

        self.fields['product_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['delivery_quantity_type'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ReservationProduct
        fields = '__all__'
        exclude = ['tied_with_reservation_of',]
