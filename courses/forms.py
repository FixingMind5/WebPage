from django import forms

from courses.models import Course
class CourseForm(forms.ModelForm):
    """Course model form"""

    class Meta:
        """Form settings"""
        model = Course
        fields = (
            'title',
            'admissionProfile',
            'dischargeProfile',
            'schedules',
            'courseLength',
            'courseDescription',
            'courseDocument',
            'courseBuilder',
            'courseCategory'
        )