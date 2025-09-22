import django_filters
from .models import Question 

class QuestionFilter(django_filters.FilterSet):
    track = django_filters.ChoiceFilter(choices=Question.Track.choices)
    level = django_filters.ChoiceFilter(choices=Question.Level.choices)
    text = django_filters.CharFilter(field_name="text", lookup_expr="icontains")

    class Meta:
        model = Question
        fields = ["track", "level", "text"]