from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shortner import views

urlpatterns = [
    path("shorten/", views.ShortenUrl.as_view(), name="shorten_url"),
    path("redir/<str:short_code>/", views.RedirectToUrl.as_view(), name="redirect_url"),
    path("slack/events/", views.SlackEventHandler.as_view(), name="slack_events"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
