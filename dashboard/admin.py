from django.contrib import admin

from .models import ChannelConfig

from .models import FetchedMessage

admin.site.register(
    ChannelConfig
)

admin.site.register(
    FetchedMessage
)