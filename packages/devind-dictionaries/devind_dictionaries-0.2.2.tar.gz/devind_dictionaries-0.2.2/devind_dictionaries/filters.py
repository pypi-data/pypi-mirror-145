"""Module description filters in dictionaies.

Last change: Luferov
Time: 2022-03-2
"""

from graphene_django_filter import AdvancedFilterSet

from .models import District, Organization, Region


class DistrictFilter(AdvancedFilterSet):
    """Class filter District."""

    class Meta:
        """Metaclass description District filter."""

        model = District
        fields = {
            'name': ('contains',),
        }


class RegionFilter(AdvancedFilterSet):
    """Class filter Regions."""

    class Meta:
        """Metaclass description Regions filter."""

        model = Region
        fields = {
            'name': ('contains',),
            'common_id': ('exact',)
        }


class OrganizationFilter(AdvancedFilterSet):
    """Class filter Organizations."""

    class Meta:
        """Metaclass description Organizations filter."""

        model = Organization
        fields = {
            'id': ('exact', 'in',),
            'parent': ('exact', 'isnull'),
            'name': ('exact', 'icontains',),
            'inn': ('exact', 'icontains',),
            'kpp': ('exact', 'icontains',),
            'kind': ('exact', 'icontains',),
            'rubpnubp': ('exact', 'icontains',),
            'kodbuhg': ('exact', 'icontains',),
            'okpo': ('exact', 'icontains',),
            'phone': ('exact', 'icontains',),
            'site': ('exact', 'icontains',),
            'mail': ('exact', 'icontains',),
            'address': ('exact', 'icontains',),
            'region': ('exact', 'in',),
            'department': ('exact', 'in',)
        }
