import slack_sdk
import json
from .models import ShortUrlModel, generate_short_code
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
import logging
import requests
import os
from dotenv import load_dotenv
load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_TOKEN')

logger = logging.getLogger(__name__)

client = slack_sdk.WebClient(
    token=SLACK_TOKEN)
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
            return redirect(original_url)  # Redirect to the original URL
        except ShortUrlModel.DoesNotExist:
            return Response({"error": "Invalid short code"}, status=404)


class SlackEventHandler(APIView):
    def post(self, request):
        data = request.data
        if data.get("type") == "url_verification":
            return Response({"challenge": data.get("challenge")})

        if data.get("event").get("type") == "message":
            message = data.get("event").get("text")
            if message[0] is not None and message[0] == "<":
                message = message[1:]
            if message[-1] is not None and message[-1] == ">":
                message = message[:-1]
            original_url = message
            user = data.get("event").get("user")
            try:
                short_url = ShortUrlModel.objects.get(original_url=original_url)
                short_code = short_url.short_code
                short_url= "https://slackurlshortner-fd74f723a2da.herokuapp.com/redir/"+ short_code
            except ShortUrlModel.DoesNotExist:
                short_code = generate_short_code(original_url)
                short_url = ShortUrlModel.objects.create(
                original_url=original_url, short_code=short_code)

            if BOT_ID != user:
                client.chat_postMessage(channel="#shortner", text=short_url)
        return Response({"shortened_url": short_url}, status=200)
