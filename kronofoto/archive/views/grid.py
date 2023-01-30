from django.shortcuts import redirect
from django.views.generic import ListView
from django.core.cache import cache
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from .basetemplate import BaseTemplateMixin
from ..models import Photo, CollectionQuery
import json


class GridBase(BaseTemplateMixin, ListView):
    model = Photo
    paginate_by = settings.GRID_DISPLAY_COUNT
    _queryset = None

    @property
    def queryset(self):
        if self._queryset is None:
            self._queryset = self.get_queryset()
        return self._queryset

    def get_paginate_by(self, qs):
        return self.request.GET.get('display', self.paginate_by)

    def render(self, context, **kwargs):
        response = super().render_to_response(context, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def render_to_response(self, context, **kwargs):
        if hasattr(self, 'redirect'):
            return self.redirect
        return self.render(context, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        for i, photo in enumerate(page_obj):
            photo.row_number = page_obj.start_index() + i - 1
        self.attach_params(page_obj)
        return context

class GridViewFormatter:
    def __init__(self, parameters):
        self.parameters = parameters
    def page_url(self, num, json=False):
        view = 'gridview-json' if json else 'gridview'
        return "{}?{}".format(reverse(view, args=(num,)), self.parameters.urlencode())

class SearchResultsViewFormatter:
    def __init__(self, parameters):
        self.parameters = parameters
    def page_url(self, num, json=False):
        params = self.parameters.copy()
        params['page'] = num
        view = 'search-results'
        return "{}?{}".format(reverse(view), params.urlencode())
    def render(self, context, **kwargs):
        return super().render_to_response(context, **kwargs)

class GridView(GridBase):
    def get_queryset(self):
        expr = self.final_expr
        self.collection = CollectionQuery(expr, self.request.user)
        qs = self.model.objects.filter_photos(self.collection).order_by('year', 'id')
        cache_info = 'photo_count:' + self.collection.cache_encoding()
        photo_count = cache.get(cache_info)
        if not photo_count:
            photo_count = qs.count()
            cache.set(cache_info, photo_count)
        if photo_count == 1:
            self.redirect = redirect(qs[0].get_absolute_url())
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatter'] = GridViewFormatter(self.request.GET)
        context['constraint'] = json.dumps({"Constraint": self.request.headers.get('Constraint', None)})

        try:
            context['timeline_url'] = context['page_obj'][0].get_absolute_url()
        except IndexError:
            pass
        return context

    def attach_params(self, photos):
        params = self.request.GET.copy()
        if 'display' in params:
            params.pop('display')
        for photo in photos:
            photo.save_params(params=params)


class SearchResultsView(GridBase):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search-form'] = self.form
        context['formatter'] = SearchResultsViewFormatter(self.request.GET)
        if not self.object_list.exists():
            context['noresults'] = True
            photo_rec = Photo.objects.filter(phototag__tag__tag='silly', phototag__accepted=True).order_by('?')[0]
            context['oops_photo'] = photo_rec
            context['query_expr'] = str(self.final_expr)
            context["tags"] = photo_rec.get_accepted_tags(self.request.user)
        else:
            context['noresults'] = False
            if self.final_expr and self.final_expr.is_collection():
                context['timeline_url'] = context['page_obj'][0].get_absolute_url()
        return context

    def attach_params(self, photos):
        params = self.request.GET.copy()
        if 'display' in params:
            params.pop('display')
        for photo in photos:
            photo.save_params(params=params)

    def dispatch(self, request, *args, **kwargs):
        if self.form.is_valid():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Invalid search parameters')

    def get_queryset(self):
        expr = self.final_expr

        if expr is None or expr.is_collection():
            self.collection = CollectionQuery(expr, self.request.user)
            qs = self.model.objects.filter_photos(self.collection).order_by('year', 'id')
        else:
            qs = expr.as_search(self.model.objects, self.request.user)
        try:
            self.redirect = redirect(qs.get().get_absolute_url())
        except (MultipleObjectsReturned, self.model.DoesNotExist):
            pass
        return qs
