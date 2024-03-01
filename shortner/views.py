import slack_sdk
import certifi
import json
from .models import ShortUrlModel, generate_short_code
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
import os
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
client = slack_sdk.WebClient(
    token="xoxb-6721483596338-6731107941204-hHuZbjq3M4L8ZWCHpt5DXvV8"
)
BOT_ID = client.api_call("auth.test")["user_id"]


class ShortenUrl(APIView):
    def post(self, request):
        original_url = request.data.get("original_url")
        if not original_url:
            return Response({"error": "Missing original URL"}, status=200)
        try:
            short_url = ShortUrlModel.objects.get(original_url=original_url)
            short_code = short_url.short_code
            return Response(
                {
                    "short_url": "https://slackurlshortner-fd74f723a2da.herokuapp.com/redir/"
                    + short_code
                }
            )
        except ShortUrlModel.DoesNotExist:
            short_code = generate_short_code(original_url)
            short_url = ShortUrlModel.objects.create(
                original_url=original_url, short_code=short_code
            )
            return Response(
                {
                    "short_url": "https://slackurlshortner-fd74f723a2da.herokuapp.com/redir/"
                    + short_code
                }
            )


class RedirectToUrl(APIView):
    def get(self, request, short_code):
        try:

            short_url = ShortUrlModel.objects.get(short_code=short_code)

            original_url = short_url.original_url
            # return Response({'original_url':original_url}, status=200)

            # return redirect(original_url)
            return redirect(original_url)  # Redirect to the original URL
        except ShortUrlModel.DoesNotExist:
            return Response({"error": "Invalid short code"}, status=404)


class SlackEventHandler(APIView):
    def post(self, request):
        payload = request.body.decode("utf-8")

        data = request.data
        json_load = json.dumps(data)
        with open("url.txt", "a") as f:
            f.write(json_load + "\n")
        if data.get("type") == "url_verification":
            return Response({"challenge": data.get("challenge")})

        if data.get("event").get("type") == "message":
            message = data.get("event").get("text")
            if message[0] is not None:
                message = message[1:]
            if message[-1] is not None:
                message = message[:-1]

            user = data.get("event").get("user")
            shortened_url = call_shorten_url(message)

            if BOT_ID != user:
                client.chat_postMessage(channel="#shortner", text=shortened_url)
        return Response({"shortened_url": data.get("event").get("text")}, status=200)


def call_shorten_url(url):
    response = requests.post(
        "https://slackurlshortner-fd74f723a2da.herokuapp.com/shorten/",
        json={"original_url": url},
        verify=False,
    )
    data = response.json()
    return data.get("short_url")
