from django import forms
from blogapp.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Write a clear article title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Share your ideas..."}),
        }
