from django.core.exceptions import BadRequest
from django.shortcuts import render
from rest_framework.generics import ListAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Max

from api.models import Consumer
from api.serializers import ConsumersFilterSerializer, ConsumersResponseSerializer
from api.pagination import LinkHeaderPagination


class Consumers(ListAPIView):
    pagination_class = LinkHeaderPagination

    def get(self, request, format=None):
        """
        Return filtered list consumers.
        """
        serializer = ConsumersFilterSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        min_previous_jobs_count = serializer.data.get("min_previous_jobs_count")
        max_previous_jobs_count = serializer.data.get("max_previous_jobs_count")
        previous_jobs_count = serializer.data.get("previous_jobs_count")
        status = serializer.data.get("status")

        qs = Consumer.objects.all()
        if status:
            qs = qs.filter(status=status)
        if previous_jobs_count and (max_previous_jobs_count or min_previous_jobs_count):
            raise BadRequest(
                "filters are conflicting can not have previous_jobs_count and max_previous_jobs_count or min_previous_jobs_count at same time")
        elif previous_jobs_count:
            qs = qs.filter(previous_jobs_count=previous_jobs_count)
        else:
            if max_previous_jobs_count:
                qs = qs.filter(previous_jobs_count__lte=max_previous_jobs_count)
            if min_previous_jobs_count:
                qs = qs.filter(previous_jobs_count__gte=min_previous_jobs_count)

        paginated_queryset = self.paginate_queryset(qs)
        paginated_response = self.get_paginated_response(ConsumersResponseSerializer(data=paginated_queryset).serialize())
        # paginated_response.data = paginated_response.data.get('results')
        return paginated_response
