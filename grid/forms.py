from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


################# for withour give option for create super user #######################
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select Group")

#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields + ('email',)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.set_password(self.cleaned_data['password1'])

#         if commit:
#             user.save()
#             user.groups.add(self.cleaned_data['group'])

#         return user


################# for create super user without group parmisson  #######################


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select Group", required=False)
    is_superuser = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'is_superuser', 'group')

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        group = cleaned_data.get('group')

        # If superuser checkbox is checked, group permission is not required
        if is_superuser:
            if group:
                self.add_error('group', 'Group permission should not be selected for superusers.')
        else:
            # If superuser checkbox is not checked, group permission is required
            if not group:
                self.add_error('group', 'This field is required if superuser checkbox is not selected.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])

        # Set user as superuser based on the checkbox
        user.is_superuser = self.cleaned_data['is_superuser']

        if commit:
            user.save()

            # Add user to the group if not a superuser
            if not user.is_superuser:
                user.groups.add(self.cleaned_data['group'])

        return user 