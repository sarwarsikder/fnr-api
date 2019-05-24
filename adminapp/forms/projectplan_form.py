from django import forms
from adminapp.models import ProjectPlans


class ProjectPlansForm(forms.ModelForm):
    title = forms.CharField(label="title", max_length=100)
    plan_file = forms.FileField(label="plan_file")
    project = forms.IntegerField(required=False)
    file_type = forms.CharField(max_length=45,required=False)
    created_by = forms.IntegerField(required=False)
    created_at = forms.DateTimeField(required=False)

    class Meta:
        model = ProjectPlans
        db_table = "project_plans"
        fields = ('title', 'plan_file', 'project', 'file_type', 'created_by')

    def clean(self):
        cleaned_data = super(ProjectPlansForm, self).clean()
        title = cleaned_data.get('title')
        if ProjectPlans.objects.filter(title=title).exclude(pk=self.instance.id).exists():
            self.add_error('title', 'Plan is already exists.')

    def save(self, request, commit=True):
        cleaned_data = super(ProjectPlansForm, self).clean()
        obj = super(ProjectPlansForm, self).save(commit=False)
        obj.created_by = request.user
        obj.file_type = cleaned_data.get('plan_file').name.split('.')[-1]
        obj.project_id = 1
        obj.save()
        return obj

    def update(self, request, commit=True):
        cleaned_data = super(ProjectPlansForm, self).clean()
        obj = super(ProjectPlansForm, self).save(commit=False)
        obj.created_by = request.user
        obj.file_type = cleaned_data.get('plan_file').name.split('.')[-1]
        obj.project_id = 1
        obj.save()
        return obj

    def process(self):
        cd = self.cleaned_data



