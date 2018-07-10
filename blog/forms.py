from .models import Comment
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from .models import Profile, Contact
from django.contrib.auth.forms import SetPasswordForm,PasswordResetForm
from django.utils.translation import ugettext_lazy as _


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username=forms.CharField( required=True,widget=forms.TextInput,max_length=30)
    first_name=forms.CharField(required=True, widget=forms.TextInput, max_length=30)
    last_name=forms.CharField(required=True, widget=forms.TextInput, max_length=30)
    email=forms.EmailField(required=True, widget=forms.EmailInput, max_length=30)
    password1=forms.CharField(required=True, label='Password', widget=forms.PasswordInput, max_length=10)
    password2=forms.CharField( required=True,label='Confirm password', widget=forms.PasswordInput,max_length=10)


    class Meta:
        model=User
        fields=('username',)

    def clean_password2(self):
        cd=self.cleaned_data

        if cd['password1']!=cd['password2']:
            raise forms.ValidationError('password did not match')
        return cd['password2']

class UserEditForm(forms.ModelForm):

    class Meta:

        model = User
        fields=['username','first_name','last_name','email']
# '''
# 	 UserEditForm : Will allow users to edit their first name, last name, and
# e-mail, which are stored in the built-in User model.
# 	 ProfileEditForm : Will allow users to edit the extra data we save in the
# custom Profile model.
# '''
class ProfileEditForm(forms.ModelForm):

    class Meta:

        model=Profile
        fields=['about_author','date_of_birth','photo']

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'



class PasswordChangeForm(SetPasswordForm):
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password




