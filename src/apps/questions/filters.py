import django_filters
from .models import Question 

class QuestionFilter(django_filters.FilterSet):
    track = django_filters.MultipleChoiceFilter(choices=Question.Track.choices)
    level = django_filters.MultipleChoiceFilter(choices=Question.Level.choices)
    has_answer = django_filters.BooleanFilter(field_name="has_answer")
    text = django_filters.CharFilter(field_name="text", lookup_expr="icontains")

    class Meta:
        model = Question
        fields = ["track", "level", "has_answer", "text"]