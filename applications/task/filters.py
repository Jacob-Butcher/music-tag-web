import django_filters


class TaskFilters(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="iexact")
    parent_path = django_filters.CharFilter(lookup_expr="iexact")
    full_path = django_filters.CharFilter(lookup_expr="startswith")
