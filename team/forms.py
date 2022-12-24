from django import forms
from .models import Coach, Athlete, Team
# Create your forms here.

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        template_name='team/team_form.html'

    name = forms.CharField()
    coaches = forms.ModelMultipleChoiceField(queryset=Coach.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    athletes = forms.ModelMultipleChoiceField(queryset=Athlete.objects.all(),
        widget=forms.CheckboxSelectMultiple)

class CoachCreateForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'bio', 'location']
        template_name='team/coach_form.html'


class AthleteCreateForm(forms.ModelForm):
    def __init(self, *args, **kwargs):
        super(AthleteCreateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('gender', 'DOB', 'profile_pic', None)
        for field in self.fields.values():
            field.widget.attrs = attrs


    class Meta:
        model = Athlete
        fields = '__all__'
        template_name='team/athlete_form.html'    
