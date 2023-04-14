from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.core.serializers.json import Serializer as DjangoCoreSerializer
from api.models import STATUS_CHOICES
import math


class ConsumersFilterSerializer(serializers.Serializer):
    min_previous_jobs_count = serializers.IntegerField(default=None)
    max_previous_jobs_count = serializers.IntegerField(default=None)
    previous_jobs_count = serializers.IntegerField(default=None)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default=None)


class ConsumersResponseSerializer:

    def __init__(self, data):
        self.data = data

    def serialize(self):
        mapped_object = {
            "type": "FeatureCollection",
            "features": [

            ]
        }

        for consumer in self.data:
            mapped_object["features"].append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [consumer.lng, consumer.lat]},
                "properties": {
                    "id": str(consumer.id),
                    "amount_due": consumer.amount_due,
                    "previous_jobs_count": consumer.previous_jobs_count,
                    "status": consumer.status,
                    "street": consumer.street
                }
            })

        return mapped_object
