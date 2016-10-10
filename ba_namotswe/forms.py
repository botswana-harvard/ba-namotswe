# from django import forms
# 
# from ba_namotswe.models import Enrollment, RegisteredSubject
# from edc_base.utils.age import age
# from edc_constants.constants import NO, YES
# from datetime import date
# 
# 
# class EnrollmentForm(forms.ModelForm):
# 
#     def clean(self):
#         self.validate_initial_visit_date()
#         self.validate_caregiver_relation_age()
#         self.validate_caregiver_relation_other()
#         self.validate_weight()
#         self.validate_height()
#         self.validate_hiv_diagnosis_date()
#         self.validate_hiv_art_initiation()
#         return self.cleaned_data
# 
#     def validate_initial_visit_date(self):
#         start_date = date(2002, 1, 1)
#         end_date = date(2016, 6, 1)
#         if self.cleaned_data.get('initial_visit_date'):
#             if self.cleaned_data.get('initial_visit_date') < start_date:
#                 raise forms.ValidationError({
#                     'initial_visit_date': [
#                         'Initial visit date should come after January 1st, 2002']})
#             elif self.cleaned_data.get('initial_visit_date') > end_date:
#                 raise forms.ValidationError({
#                     'initial_visit_date': [
#                         'Initial visit date should come before June 1st, 2016']})
#         return self.cleaned_data
# 
#     def validate_weight(self):
#         if self.cleaned_data.get('weight_measured') == NO:
#             if self.cleaned_data.get('weight'):
#                 raise forms.ValidationError({
#                     'weight': [
#                         'You should not enter weight']})
#         elif self.cleaned_data.get('weight_measured') == YES:
#             if not self.cleaned_data.get('weight'):
#                 raise forms.ValidationError({
#                     'weight': [
#                         'You should enter the weight']})
#             self.ensure_right_weight()
#         return self.cleaned_data
# 
#     def ensure_right_weight(self):
#         if self.cleaned_data.get('weight') > 136:
#                 raise forms.ValidationError({
#                     'weight': [
#                         'Weight should be less than 136 kilos']})
#         elif self.cleaned_data.get('weight') < 20:
#                 raise forms.ValidationError({
#                     'weight': [
#                         'Weight should be greater than 20 kilos']})
#         return self.cleaned_data
# 
#     def validate_height(self):
#         if self.cleaned_data.get('height_measured') == NO:
#             if self.cleaned_data.get('height'):
#                 raise forms.ValidationError({
#                     'height': [
#                         'You should not enter height']})
#         elif self.cleaned_data.get('height_measured') == YES:
#             if not self.cleaned_data.get('height'):
#                 raise forms.ValidationError({
#                     'height': [
#                         'You should enter the height']})
#             self.ensure_right_height()
#         return self.cleaned_data
# 
#     def ensure_right_height(self):
#         if self.cleaned_data.get('height') > 244:
#                 raise forms.ValidationError({
#                     'height': [
#                         'Height should be less than 244cm']})
#         elif self.cleaned_data.get('height') < 100:
#                 raise forms.ValidationError({
#                     'height': [
#                         'Height should be greater than 100cm']})
#         return self.cleaned_data
# 
#     def validate_caregiver_relation_age(self):
#         registered_subject = self.cleaned_data.get('registered_subject')
#         if registered_subject:
#             if self.cleaned_data.get('initial_visit_date'):
#                 age_at_visit = age(registered_subject.dob, self.cleaned_data.get('initial_visit_date')).years
#                 if (age_at_visit >= 10) & (age_at_visit <= 13):
#                     if not self.cleaned_data.get('caregiver_relation'):
#                         raise forms.ValidationError({
#                             'caregiver_relation': [
#                                 'Subject was between 10 and 13, you have to provide']})
#                     elif self.cleaned_data.get('caregiver_relation') == 'not_applicable':
#                         raise forms.ValidationError({
#                             'caregiver_relation': [
#                                 'Subject was between 10 and 13 years of age, you have to provide caregiver']})
#         return self.cleaned_data
# 
#     def validate_caregiver_relation_other(self):
#         if self.cleaned_data.get('caregiver_relation') != 'OTHER':
#             if self.cleaned_data.get('caregiver_relation_other'):
#                 raise forms.ValidationError({
#                     'caregiver_relation_other': [
#                         'You should not enter other caregiver relation as you have already entered a caregiver relation']})
#         else:
#             if not self.cleaned_data.get('caregiver_relation_other'):
#                 raise forms.ValidationError({
#                     'caregiver_relation_other': [
#                         'You should enter other caregiver relation as you have selected OTHER caregiver relation']})
#         return self.cleaned_data
# 
#     def validate_hiv_diagnosis_date(self):
#         if self.cleaned_data.get('registered_subject'):
#             if self.cleaned_data.get('hiv_diagnosis_date'):
#                 if self.cleaned_data.get('hiv_diagnosis_date') < self.cleaned_data.get('registered_subject').dob:
#                     raise forms.ValidationError({
#                         'hiv_diagnosis_date': [
#                             'Diagnosis date should come after date of birth']})
#         return self.cleaned_data
# 
#     def validate_hiv_art_initiation(self):
#         if self.cleaned_data.get('art_initiation_date'):
#             print(self.cleaned_data.get('art_initiation_date'))
#             if self.cleaned_data.get('hiv_diagnosis_date'):
#                 print(self.cleaned_data.get('hiv_diagnosis_date'))
#                 if self.cleaned_data.get('art_initiation_date') < self.cleaned_data.get('hiv_diagnosis_date'):
#                     print(self.cleaned_data.get('hiv_diagnosis_date'))
#                     raise forms.ValidationError({
#                         'art_initiation_date': [
#                             'ART Initiation date should come after diagnosis date']})
#         return self.cleaned_data
# 
#     class Meta:
#         model = Enrollment
#         fields = '__all__'
# 
# 
# class RegisteredSubjectForm(forms.ModelForm):
# 
#     def clean(self):
#         self.validate_dob()
#         return self.cleaned_data
# 
#     def validate_dob(self):
#         if age(self.cleaned_data['dob'], date.today()).years < 10:
#             raise forms.ValidationError({
#                 'dob': [
#                     'Date of birth should be at least 10 years ago']})
# 
#     class Meta:
#         model = RegisteredSubject
#         fields = '__all__'
