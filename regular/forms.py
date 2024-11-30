from app.models import ReservationModel
from django import forms

class MyReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyReservationForm, self).__init__(*args, **kwargs)
        self.fields['date_reserved'].label = 'Date'
        if 'location' in self.fields:
            self.fields['location'].widget.attrs['readonly'] = True
        
        if 'date_reserved' in self.fields:
            self.fields['date_reserved'].widget.attrs['placeholder'] = 'MM/DD/YYYY'

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": ""})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"rows": 1, "class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ReservationModel
        fields = "__all__"
        widget = {
            'location': forms.TextInput(attrs={'readonly':'readonly'}),
            "date_reserved": forms.DateInput(
                attrs={"type": "text", "placeholder": "MM/DD/YYYY"}
            ),
        }
        exclude = ["reserved_by","reservation_status","is_delivered","truck","is_cancelled"]