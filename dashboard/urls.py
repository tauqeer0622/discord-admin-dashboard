from django.urls import path

from .views import (
    home,
    discord_login,
    discord_callback,
    guild_channels,
    save_config,
    get_configs,
    configs_page,
    delete_config,
    toggle_config,
    logout_view,
    message_webhook,
    messages_page,
    get_channels
)

urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "login/",
        discord_login,
        name="discord_login"
    ),

    path(
        "callback/",
        discord_callback,
        name="callback"
    ),

    path(
        "guild/<str:guild_id>/channels/",
        guild_channels,
        name="guild_channels"
    ),
    path(
        "save-config/",
        save_config,
        name="save_config"
    ),
    path(
        "api/configs/",
        get_configs,
        name="get_configs"
    ),
    path(
        "configs/",
        configs_page,
        name="configs_page"
    ),

    path(
        "delete-config/<int:config_id>/",
        delete_config,
        name="delete_config"
    ),
    path(
        "toggle-config/<int:config_id>/",
        toggle_config,
        name="toggle_config"
    ),
    path(
        "logout/",
        logout_view,
        name="logout"
    ),
    path(
        "webhook/messages/",
        message_webhook,
        name="message_webhook"
    ),
    path(
        "messages/",
        messages_page,
        name="messages_page"
    ),
    path(
        "api/channels/<str:guild_id>/",
        get_channels,
        name="get_channels"
    ),
    ]