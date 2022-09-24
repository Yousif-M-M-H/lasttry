from django.forms import ModelForm
from .models import Myname


class NameForm(ModelForm):
    class Meta:
        model = Myname
        fields = '__all__'
