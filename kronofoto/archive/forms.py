from django import forms
from .models import Tag, PhotoTag, Collection, Term, Donor, Photo
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .search import expression
from .search.parser import Parser, NoExpression
from functools import reduce


generate_choices = lambda field: lambda: [('', field.capitalize())] + [(p[field], p[field]) for p in Photo.objects.exclude(**{field: ''}).values(field).distinct().order_by(field)]


class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    term = forms.ModelChoiceField(required=False, queryset=Term.objects.all().order_by('term'))
    startYear = forms.IntegerField(required=False)
    endYear = forms.IntegerField(required=False)
    donor = forms.ModelChoiceField(required=False, queryset=Donor.objects.all().order_by('last_name', 'first_name'))
    city = forms.ChoiceField(required=False, choices=generate_choices('city'))
    county = forms.ChoiceField(required=False, choices=generate_choices('county'))
    state = forms.ChoiceField(required=False, choices=generate_choices('state'))
    country = forms.ChoiceField(required=False, choices=generate_choices('country'))
    def as_expression(self):
        form_exprs = []
        try:
            parser = Parser.tokenize(self.cleaned_data['query'])
            form_exprs.append(parser.parse().shakeout())
        except NoExpression:
            pass
        except:
            try:
                form_exprs.append(parser.simple_parse().shakeout())
            except NoExpression:
                pass
        startYear = endYear = None
        if self.cleaned_data['term']:
            form_exprs.append(expression.TermExactly(self.cleaned_data['term']))
        if self.cleaned_data['startYear']:
            startYear = expression.YearGTE(self.cleaned_data['startYear'])
        if self.cleaned_data['endYear']:
            endYear = expression.YearLTE(self.cleaned_data['endYear'])
        if startYear and endYear:
            form_exprs.append(startYear & endYear)
        elif startYear:
            form_exprs.append(startYear)
        elif endYear:
            form_exprs.append(endYear)
        if self.cleaned_data['donor']:
            form_exprs.append(expression.DonorExactly(self.cleaned_data['donor']))
        if self.cleaned_data['city']:
            form_exprs.append(expression.City(self.cleaned_data['city']))
        if self.cleaned_data['state']:
            form_exprs.append(expression.State(self.cleaned_data['state']))
        if self.cleaned_data['country']:
            form_exprs.append(expression.Country(self.cleaned_data['country']))
        if len(form_exprs):
            return reduce(expression.Or, form_exprs)
        raise NoExpression


class RegisterUserForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Verify Password', widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        if 'email' in data and User.objects.filter(username=data['email']).exists():
            self.add_error('email', 'There is already an account associated with that email address.')
        if 'password1' in data:
            validate_password(data['password1'])
            if 'password2' not in data or data['password1'] != data['password2']:
                self.add_error('password1', 'The password fields must be identical')
        return data


class TagForm(forms.Form):
    tag = forms.CharField()

    def add_tag(self, photo):
        tag, _ = Tag.objects.get_or_create(tag=self.cleaned_data['tag'])
        phototag = PhotoTag.objects.get_or_create(tag=tag, photo=photo, defaults={'accepted': False})


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'visibility']


class AddToListForm(forms.Form):
    collection = forms.ChoiceField(required=False)
    name = forms.CharField(required=False)
    visibility = forms.ChoiceField(required=False, choices=Collection.PRIVACY_TYPES)

    def __init__(self, *args, **kwargs):
        self.collection = kwargs.pop('collections')
        super().__init__(*args, **kwargs)
        self.fields['collection'].choices = self.collection

    def clean(self):
        data = super().clean()
        if not data['collection'] and not data['name']:
            self.add_error('name', 'A name must be provided')
        return data
