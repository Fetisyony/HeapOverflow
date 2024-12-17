from django import forms
from .models import Answer, Profile, Question, Tag
from django.contrib.auth.models import User
from .management.commands.fill_db import pull_of_tags

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if (not username):
            raise forms.ValidationError("Please fill out that field")

        return username
    
    def clean_password(self):
        password = self.cleaned_data['password'].strip()

        if (not password):
            raise forms.ValidationError("Please fill out that field")

        return password

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
    
class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your login',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )
    repeat_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
        })
    )

    class Meta:
        model = Profile
        fields = []
    
    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if (not username):
            raise forms.ValidationError("Please fill out that field")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if (len(password) < 8):
            raise forms.ValidationError("Password must be at least 8 characters long")
        
        if (not password):
            raise forms.ValidationError("Please fill out that field")

        return password
    
    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        
        if (not repeat_password):
            raise forms.ValidationError("Please fill out that field")
        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match.")
        return repeat_password
    
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            profile = super().save(commit=False)
            profile.user = user
            profile.save()
        
        return user

class AnswerForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer here',
        })
    )

    class Meta:
        model = Answer

        fields = ('body',)

    def clean_body(self):
        body = self.cleaned_data['body'].strip()

        if (not body):
            raise forms.ValidationError("You can't post an empty answer")

        return body

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, profile, question_id):
        answer = super().save(commit=False)
        answer.user = profile
        answer.question_id = question_id
        answer.save()

        return answer.id


class NewQuestionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. How to center div?',
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Here explain in details your problem',
        })
    )
    tags_input = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by space',
        })
    )

    class Meta:
        model = Question

        fields = ('title', 'body')

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if (not title):
            raise forms.ValidationError("Please fill out that field")

        return title

    def clean_body(self):
        body = self.cleaned_data['body'].strip()

        if (not body):
            raise forms.ValidationError("Please fill out that field")

        return body

    def clean_tags_input(self):
        tags_raw_input = self.cleaned_data['tags_input'].strip()

        tag_names = [name.strip() for name in tags_raw_input.split(' ') if name.strip()]

        unique_tag_names = set(tag_names)

        if (len(unique_tag_names) != len(tag_names)):
            raise forms.ValidationError("Tags must be unique")
        if (len(unique_tag_names) < 3):
            raise forms.ValidationError("Put here at least 3 tags separated by space")
        
        for tag_name in tag_names:
            if (tag_name not in pull_of_tags):
                raise forms.ValidationError(f"Unknown tag: {tag_name}")

        tags = [Tag.objects.get(name=tag_name) for tag_name in tag_names]
        return tags

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, profile):
        question = super().save(commit=False)
        question.user = profile
        question.save()
        question.tags.set(self.cleaned_data.get('tags_input', []))

        return question.id
