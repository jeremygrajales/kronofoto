from django import forms
from .widgets import RecaptchaWidget, AutocompleteWidget
from django.conf import settings
from django.core.exceptions import ValidationError
import urllib
import json
import re

archive_id_tag = re.compile(r"\[\s*([^\[\]]*[^\[\]\s]+)\s*-\s*(\d+)\s*\]")
id_tag = re.compile(r"\[\s*(\d+)\s*\]")


class AutocompleteField(forms.CharField):
    def __init__(self, *args, queryset, to_field_name="pk", widget=AutocompleteWidget, **kwargs):
        super().__init__(*args, widget=widget, **kwargs)
        self.queryset = queryset
        self.to_field_name = to_field_name

    def to_python(self, value):
        value = super().to_python(value)

        for match in reversed(list(re.finditer(archive_id_tag, value))):
            start = match.start()
            archive = match.group(1).lower()
            id = int(match.group(2))

            objs = self.queryset.filter(**{self.to_field_name: id})
            if not objs.exists():
                raise ValidationError("No object with that ID was found.")
            obj = objs[0]

            if obj.archive.slug != archive:
                raise ValidationError("That ID is in the archive {}.".format(obj.archive.slug))
            namestuff = value[0:start].lower()
            if obj.first_name.lower() not in namestuff or obj.last_name.lower() not in namestuff:
                raise ValidationError("That id matches {}.".format(obj.display_format()))
            return obj

        for match in reversed(list(re.finditer(id_tag, value))):
            id = int(match.group(1))
            objs = self.queryset.filter(**{self.to_field_name: id})
            if not objs.exists():
                raise ValidationError("No object with that ID was found.")
            return objs[0]
        if value.strip() == "":
            return None
        raise ValidationError("Could not find an ID.")


class RecaptchaField(forms.CharField):
    widget = RecaptchaWidget
    def __init__(self, required_score=0.7, label=False, *args, **kwargs):
        super().__init__(label=label, *args, **kwargs)
        self.required = True
        self.widget.attrs['data-sitekey'] = settings.GOOGLE_RECAPTCHA3_SITE_KEY
        self.required_score = required_score

    def check_captcha(self, value):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA3_SECRET_KEY,
            'response': value,
        }
        args = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request('https://www.google.com/recaptcha/api/siteverify', data=args)
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    def validate(self, value):
        super().validate(value)
        result = self.check_captcha(value)
        if not result['success']:
            raise ValidationError("Captcha failure")
        if result['score'] < self.required_score:
            raise ValidationError("Captcha failure")

