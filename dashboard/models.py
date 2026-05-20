from django.db import models

class ChannelConfig(models.Model):

    guild_id = models.CharField(
        max_length=255
    )

    guild_name = models.CharField(
        max_length=255
    )

    channel_id = models.CharField(
        max_length=255
    )

    channel_name = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "guild_id",
            "channel_id"
        )

    def __str__(self):

        return (
            f"{self.guild_name} "
            f"- "
            f"{self.channel_name}"
        )

class FetchedMessage(models.Model):

    source_label = models.CharField(
        max_length=255
    )

    author = models.CharField(
        max_length=255
    )

    content = models.TextField()

    timestamp = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.author} "
            f"- "
            f"{self.source_label}"
        )