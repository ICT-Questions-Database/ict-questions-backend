from rest_framework.pagination import PageNumberPagination

class SubmissionPagination(PageNumberPagination):
    page_size = 5