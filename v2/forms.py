from django import forms
from v2.models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments

        fields = (
            'name',
            'content',
        )