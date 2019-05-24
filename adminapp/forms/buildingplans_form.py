from django import forms
from adminapp.models import  BuildingPlans


class BuildingPlansForm(forms.ModelForm):
    title = forms.CharField(label="title",max_length=100)
    plan_file = forms.FileField(label="plan_file", required=False)
    building = forms.IntegerField(required=False)
    file_type = forms.CharField(max_length=45,required=False)
    created_by = forms.IntegerField(required=False)
    created_at = forms.DateTimeField(required=False)

    class Meta:
        model = BuildingPlans
        db_table = "building_plans"
        fields = ('title', 'plan_file', 'building', 'file_type', 'created_by')


    def clean(self):
        cleaned_data = super(BuildingPlansForm, self).clean()
        title = cleaned_data.get('title')
        if BuildingPlans.objects.filter(title=title).exclude(pk=self.instance.id).exists():
            self.add_error('title', 'Plan is already exists.')

    def save(self, request, commit=True):
        cleaned_data = super(BuildingPlansForm, self).clean()
        obj = super(BuildingPlansForm, self).save(commit=False)
        obj.created_by = request.user
        obj.file_type = cleaned_data.get('plan_file').name.split('.')[-1]
        obj.building_id = 3
        obj.save()
        return obj

    def update(self, request, commit=True):
        cleaned_data = super(BuildingPlansForm, self).clean()
        obj = super(BuildingPlansForm, self).save(commit=False)
        obj.created_by = request.user
        obj.file_type = cleaned_data.get('plan_file').name.split('.')[-1]
        obj.building_id = 3
        obj.save()
        return obj

    def process(self):
        cd = self.cleaned_data



