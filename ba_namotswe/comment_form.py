from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from django import forms
from django.urls.base import reverse


class CommentForm(forms.Form):

    comment = forms.CharField(
        label='',
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('dashboard')
        self.helper.form_id = 'form-comment'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            FieldWithButtons('comment', StrictButton('Save', type='submit')))
