

class MarqueeViewMixin:

    def __init__(self):
        self.context = {}
        self.markey_next_row = 15
        self.consent_model = None

    def get_context_data(self, **kwargs):
        self.context = super(MarqueeViewMixin, self).get_context_data(**kwargs)
        return self.context

    @property
    def markey_data(self):
        markey_data = {}
        if self.enrollment:
            markey_data = {
                'Initials': '{}'.format(self.enrollment.initials),
                'Born': self.enrollment.dob,
                'Age': self.age,
                'Gender': self.gender,
                'Height': self.enrollment.height,
                'Weight': self.enrollment.weight,
                'Identifier': self.enrollment.subject_identifier,
            }
        return markey_data

    @property
    def enrollment(self):
        return self.enrollment_model

    @property
    def age(self):
        return None

    @property
    def age_today(self):
        return None

    @property
    def gender(self):
        gender = 'Female' if self.enrollment.gender == 'F' else 'Male'
        return gender
