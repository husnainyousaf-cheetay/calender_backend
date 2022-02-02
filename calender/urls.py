from django.urls import path
from graphene_django.views import GraphQLView
from calender.schema import schema

urlpatterns = [
    path('graphiql', GraphQLView.as_view(graphiql=True, schema=schema)),
]
