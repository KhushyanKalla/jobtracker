# jobs/filters.py ← CREATE this new file
import django_filters
from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):

    # Salary range filters
    min_salary = django_filters.NumberFilter(
        field_name='salary',
        lookup_expr='gte'   # gte = greater than or equal
    )
    max_salary = django_filters.NumberFilter(
        field_name='salary',
        lookup_expr='lte'   # lte = less than or equal
    )

    # Date range
    applied_after = django_filters.DateFilter(
        field_name='date_applied',
        lookup_expr='gte'
    )

    class Meta:
        model = JobApplication
        fields = ['status', 'company', 'min_salary', 'max_salary']