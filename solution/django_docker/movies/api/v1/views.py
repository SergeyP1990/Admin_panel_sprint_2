from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, RoleType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type')\
            .annotate(genres=ArrayAgg('genres__name', distinct=True))\
            .annotate(actors=ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=RoleType.ACTOR)))\
            .annotate(directors=ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=RoleType.DIRECTOR)))\
            .annotate(writers=ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=RoleType.WRITER)))
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        next_page=None
        prev_page=None
        if page.has_next():
            next_page = page.next_page_number()
        if page.has_previous():
            prev_page = page.previous_page_number()

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev_page,
            'next': next_page,
            'results': list(queryset),
        }
        return context

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.get_object()



