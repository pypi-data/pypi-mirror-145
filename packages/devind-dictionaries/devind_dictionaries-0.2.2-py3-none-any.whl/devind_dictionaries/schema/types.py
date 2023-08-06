"""Graphql Types for dictionaries."""

import graphene
from devind_helpers.optimized import OptimizedDjangoObjectType
from devind_helpers.schema.connections import CountableConnection
from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene_django_optimizer import resolver_hints
from graphql import ResolveInfo

from ..filters import DistrictFilter, OrganizationFilter, RegionFilter
from ..models import Department, District, Organization, Region
from ..settings import dictionaries_settings


class DepartmentType(DjangoObjectType):
    """Object type for Department."""

    user = graphene.Field(dictionaries_settings.USER_TYPE, required=True, description='Director of department.')
    minister = graphene.Field(dictionaries_settings.USER_TYPE, required=True, description='Responsible Minister.')
    users = graphene.List(dictionaries_settings.USER_TYPE, description='Department staff.')
    organizations = graphene.List(lambda: OrganizationType, description='Organizations.')

    class Meta:
        """Metaclass with description parameters."""

        model = Department
        fields = (
            'id',
            'name',
            'code',
            'created_at',
            'updated_at',
            'user',
            'minister',
            'users',
            'organizations',
        )

    @staticmethod
    @resolver_hints(model_field='users')
    def resolve_users(department: Department, info: ResolveInfo, *args, **kwargs) -> QuerySet:
        """Resolve function for users in Departments."""
        return department.users.all()

    @staticmethod
    def resolve_organizations(department: Department, info: ResolveInfo, *args, **kwargs) -> QuerySet:
        """Resolve function for organizations in Departments."""
        return department.organizations.all()


class DistrictType(DjangoObjectType):
    """Object type for District."""

    regions = graphene.List(lambda: RegionType, description='List of regions.')

    class Meta:
        """Metaclass with description parameters."""

        model = District
        fields = ('id', 'name', 'created_at', 'updated_at', 'regions',)
        filterset_class = DistrictFilter

    @staticmethod
    @resolver_hints(model_field='region_set')
    def resolve_regions(district: District, info: ResolveInfo, *args, **kwargs) -> QuerySet[Region]:
        """Resolve function for Regions in District."""
        return district.region_set.all()


class RegionType(DjangoObjectType):
    """Object type for Regions."""

    class Meta:
        """Metaclass with description parameters."""

        model = Region
        fields = ('id', 'name', 'common_id', 'created_at', 'updated_at', 'district',)
        filterset_class = RegionFilter


class OrganizationType(OptimizedDjangoObjectType):
    """Optimized type for Organizations."""

    departments = graphene.List(DepartmentType, description='Departments.')

    class Meta:
        """Metaclass with description parameters."""

        model = Organization
        interfaces = (graphene.relay.Node,)
        fields = (
            'name', 'present_name',
            'inn', 'kpp', 'kind',
            'rubpnubp', 'kodbuhg', 'okpo',
            'phone', 'site', 'mail', 'address',
            'attributes',
            'created_at', 'updated_at',
            'parent',
            'region',
            'departments'
        )
        filterset_class = OrganizationFilter
        connection_class = CountableConnection

    @staticmethod
    @resolver_hints(model_field='department_set')
    def resolve_departments(organization: Organization, info: ResolveInfo, *args, **kwargs) -> QuerySet:
        """Resolve function for get departments of organizations."""
        return organization.department_set.all()
