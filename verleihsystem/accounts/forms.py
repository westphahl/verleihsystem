from django.forms import ModelForm

from accounts.models import UserProfile


class UserProfileForm(ModelForm):
    """
    Form for the user profile model.
    """

    class Meta:
        model = UserProfile
        exclude = ('user', 'picture',)
