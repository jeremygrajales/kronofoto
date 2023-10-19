from django.forms.widgets import NumberInput, Widget
from django.forms import MultiWidget, HiddenInput

class AutocompleteWidget(Widget):
    template_name = "archive/widgets/autocomplete.html"

    def __init__(self, *args, url, **kwargs):
        self.url = url
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = 'text'
        context['url'] = self.url
        return context

class RecaptchaWidget(Widget):
    template_name = 'archive/widgets/captcha.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['public_key'] = self.attrs['data-sitekey']
        return context

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)

class HeadingWidget(NumberInput):
    sphere_width = 600
    sphere_height = 400

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        self.template_name = 'archive/widgets/heading.html'
        context['sphere_image'] = self.attrs['photo']
        context['id'] = attrs['id']
        context['sphere_width'] = self.sphere_width
        context['sphere_height'] = self.sphere_height
        context['module'] = 'archive_heading'
        return context

class PositioningWidget(MultiWidget):
    sphere_width = 600
    sphere_height = 800

    def __init__(self, attrs=None, **kwargs):
        widgets = (
            NumberInput(attrs=dict(anglename="azimuth")),
            NumberInput(attrs=dict(anglename="inclination")),
            NumberInput(attrs=dict(anglename="distance")),
        )
        super().__init__(widgets=widgets, attrs=attrs, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if 'photosphere' in self.attrs:
            self.template_name = 'archive/widgets/positioning.html'
            context['sphere_image'] = self.attrs['photosphere']
            context['photo'] = self.attrs['photo']
            context['photo_h'] = self.attrs['photo_h']
            context['photo_w'] = self.attrs['photo_w']
            context['id'] = attrs['id']
            context['sphere_width'] = self.sphere_width
            context['sphere_height'] = self.sphere_height
        return context

    def decompress(self, value):
        if value:
            return [value['azimuth'], value['inclination'], value['distance']]
        return [0, 0, 500]
