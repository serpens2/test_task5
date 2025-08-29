from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows":5}),
            "source": forms.TextInput(attrs={"class": "form-control"}),
            "weight": forms.Select(attrs={"class": "form-select"}),
        }
    def clean_text(self):
        text = self.data["text"]
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует!")
        return text
    def clean_source(self):
        source = self.data["source"]
        if Quote.objects.filter(source=source).count() >= 3:
            raise forms.ValidationError("У этого источника уже есть 3 цитаты!")
        return source
