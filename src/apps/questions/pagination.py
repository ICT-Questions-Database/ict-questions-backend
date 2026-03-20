from rest_framework.pagination import PageNumberPagination


class QuestionsPagination(PageNumberPagination):
    page_size = 20