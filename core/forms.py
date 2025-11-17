from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Votre nom', 'id': 'userName'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Votre email', 'id': 'userEmail'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Votre téléphone', 'id': 'userPhone'})
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Objet de la demande', 'id': 'messageSubject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Décrivez votre projet ou besoin', 'id': 'userMessage', 'rows': 5})
    )

    # Nous gardons les noms de classe du template original pour le style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-input'})
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['phone'].widget.attrs.update({'class': 'form-input'})
        self.fields['subject'].widget.attrs.update({'class': 'form-input'})
        self.fields['message'].widget.attrs.update({'class': 'form-input message-input'})


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Votre email'})
    )