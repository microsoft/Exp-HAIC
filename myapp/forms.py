from django import forms


class diagnosisform2(forms.Form):
    presence = forms.ChoiceField(
                widget=forms.RadioSelect(
                    attrs={"class": "form-check-input", "id": "hi"}
                ),
                choices=[("no", "no"), ("yes", "yes")],
            )


class diagnosisform(forms.Form):
    def __init__(self, *args, **kwargs):
        n_diagnoses = kwargs.pop("n_diagnoses")
        super(diagnosisform, self).__init__(*args, **kwargs)
        for i in range(n_diagnoses):
            # self.fields['i' + str(i)] =  forms.CharField(label=i)
            self.fields["i" + str(i)] = forms.ChoiceField(
                widget=forms.RadioSelect(
                    attrs={"class": "form-check-input", "id": "hi" + str(i)}
                ),
                choices=[("no", "no"), ("yes", "yes")],
            )
    # answer = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'hi'}), choices=CHOICES)
    # https://stackoverflow.com/questions/17159567/how-to-create-a-list-of-fields-in-django-forms


class SignupForm(forms.Form):
	#django gives a number of predefined fields
	#CharField and EmailField are only two of them
	#go through the official docs for more field details
	name = forms.CharField(label='Enter your name', max_length=100)


# https://techincent.com/render-django-form-individual-fields-manually/