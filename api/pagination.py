from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlencode


class LinkHeaderPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        base_url = self.request.build_absolute_uri()
        page_number = self.page.number
        page_size = self.get_page_size(self.request)
        total_count = self.page.paginator.count
        last_page = self.page.paginator.num_pages

        links = []
        if page_number > 1:
            links.append(
                '<{}?{}>; rel="prev"'.format(base_url, urlencode({'page': page_number - 1, 'page_size': page_size})))
        if page_number < last_page:
            links.append(
                '<{}?{}>; rel="next"'.format(base_url, urlencode({'page': page_number + 1, 'page_size': page_size})))
        links.append('<{}?{}>; rel="last"'.format(base_url, urlencode({'page': last_page, 'page_size': page_size})))
        links.append('<{}?{}>; rel="first"'.format(base_url, urlencode({'page': 1, 'page_size': page_size})))

        headers = {
            'Link': ', '.join(links)
        }
        return Response(data, headers=headers)
