import requests

import json

from django.shortcuts import render, redirect
from django.conf import settings
from .models import (
    ChannelConfig,
    FetchedMessage
)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt



def home(request):

    total_configs = (
        ChannelConfig.objects.count()
    )

    active_configs = (
        ChannelConfig.objects.filter(
            is_active=True
        ).count()
    )

    disabled_configs = (
        ChannelConfig.objects.filter(
            is_active=False
        ).count()
    )

    return render(

        request,

        "home.html",

        {
            "total_configs": total_configs,

            "active_configs": active_configs,

            "disabled_configs": disabled_configs
        }
    )


def discord_login(request):

    discord_url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={settings.DISCORD_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={settings.DISCORD_REDIRECT_URI}"
        "&scope=identify guilds"
    )

    return redirect(discord_url)


def discord_callback(request):

    code = request.GET.get("code")

    token_url = "https://discord.com/api/oauth2/token"

    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.DISCORD_REDIRECT_URI,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_response = requests.post(
        token_url,
        data=data,
        headers=headers
    )

    token_json = token_response.json()

    access_token = token_json.get(
        "access_token"
    )

    request.session[
        "discord_access_token"
    ] = access_token

    # Fetch guilds/servers

    guilds_response = requests.get(

        "https://discord.com/api/users/@me/guilds",

        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    guilds = guilds_response.json()
    request.session["guilds"] = guilds
    return redirect("/guilds/")

def guild_channels(request, guild_id):


    access_token = request.session.get(
        "discord_access_token"
    )

    response = requests.get(

        f"https://discord.com/api/guilds/{guild_id}/channels",

        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    channels = response.json()
    print(channels)

    return render(

        request,

        "channels.html",

        {
            "channels": channels
        }
    )
@login_required
def save_config(request):

    if request.method == "POST":

        guild_id = request.POST.get(
            "guild_id"
        )

        guild_name = request.POST.get(
            "guild_name"
        )

        channel_id = request.POST.get(
            "channel_id"
        )

        channel_name = request.POST.get(
            "channel_name"
        )

        ChannelConfig.objects.get_or_create(

            guild_id=guild_id,

            guild_name=guild_name,

            channel_id=channel_id,

            channel_name=channel_name
        )

        messages.success(
            request,
            "Configuration saved successfully"
        )

        return redirect("/configs/")

    return redirect("/")

@login_required
def get_configs(request):

    configs = ChannelConfig.objects.all()

    payload = []

    for config in configs:

        payload.append({

            "label": (
                f"{config.guild_name} "
                f"- "
                f"{config.channel_name}"
            ),

            "channel_id": config.channel_id
        })

    return JsonResponse(
        payload,
        safe=False
    )

@login_required
def configs_page(request):

    configs = ChannelConfig.objects.all()

    return render(

        request,

        "configs.html",

        {
            "configs": configs
        }
    )

@login_required
def delete_config(request, config_id):

    config = ChannelConfig.objects.get(
        id=config_id
    )

    config.delete()
    messages.success(
        request,
        "Configuration deleted"
    )

    return redirect("/configs/")

@login_required
def toggle_config(request, config_id):

    config = ChannelConfig.objects.get(
        id=config_id
    )

    config.is_active = (
        not config.is_active
    )

    config.save()
    messages.success(
        request,
        "Configuration updated"
    )

    return redirect("/configs/")

def logout_view(request):

    logout(request)

    return redirect("/admin/login/")


@csrf_exempt
def message_webhook(request):

    if request.method == "POST":

        data = json.loads(
            request.body
        )

        for source_label, messages in data.items():

            for message in messages:

                FetchedMessage.objects.create(

                    source_label=source_label,

                    author=message.get(
                        "author"
                    ),

                    content=message.get(
                        "content"
                    ),

                    timestamp=message.get(
                        "timestamp"
                    )
                )

        return JsonResponse({

            "status": "success"

        })

    return JsonResponse({

        "error": "Invalid request"

    })


@login_required
def messages_page(request):

    messages = (
        FetchedMessage.objects
        .all()
        .order_by("-timestamp")[:50]
    )

    return render(

        request,

        "messages.html",

        {
            "messages": messages
        }
    )

@login_required
def guilds_channel(request):

    guilds = request.session.get(
        "guilds",
        []
    )

    if request.method == "POST":

        guild_id = request.POST.get(
            "guild_id"
        )

        guild_name = request.POST.get(
            "guild_name"
        )

        channel_id = request.POST.get(
            "channel_id"
        )

        channel_name = request.POST.get(
            "channel_name"
        )

        if channel_id:

            ChannelConfig.objects.get_or_create(

                guild_id=guild_id,

                guild_name=guild_name,

                channel_id=channel_id,

                channel_name=channel_name
            )

            return redirect("/configs/")

    return render(

        request,

        "guilds.html",

        {
            "guilds": guilds
        }
    )
# def get_channels(request, guild_id):
#     # TODO:
#     # Replace temporary channel mapping
#     # with real Discord API channel fetching
#
#     channels = [
#
#         {
#             "id": "1506591836020412589",
#             "name": "test"
#         }
#
#     ]
#
#     return JsonResponse(
#         channels,
#         safe=False
#     )
