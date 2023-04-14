import datetime
import json
import logging
import threading

from django.conf import settings
from django.core.management import BaseCommand
import csv
from api.models import Consumer
from django.db.models import Q
from django.db import connection

logger = logging.getLogger("django.populate_consumers_data")

MAX_NO_OF_THREADS = 100


def insert_data_to_db(data):
    consumer = Consumer(
        id=data[0],
        street=data[1],
        status=data[2],
        previous_jobs_count=data[3],
        amount_due=data[4],
        lat=data[5],
        lng=data[6]
    )
    consumer.save()
    logger.info(f"data with id {data[0]} is saved")
    connection.close()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        start_time = datetime.datetime.now()

        Consumer.objects.all().delete()
        if Consumer.objects.all().count() > 0:
            logger.info("Error consumers data is not empty")
            exit()

        threads = []
        with open('initial_data/consumers.csv') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                threads.append(threading.Thread(target=insert_data_to_db, args=(row,)))
                threads[-1].start()

                if len(threads) > MAX_NO_OF_THREADS:
                    while len(threads) > 0:
                        threads.pop().join()


        endtime = datetime.datetime.now()

        total_time = endtime - start_time

        logger.info("Total Time is "+str(total_time))
