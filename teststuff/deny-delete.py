import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class DenyDeleteCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="deny-delete", description="Deletes the current channel after a few seconds.")
    @app_commands.describe(reason="The reason for deleting this channel (optional).")
    @app_commands.checks.has_permissions(manage_channels=True) # Manage channels for safety
    async def deny_delete(self, interaction: discord.Interaction, reason: str | None = None):
        no_mentions = discord.AllowedMentions.none()

        if interaction.channel is None or interaction.channel.type not in (
            discord.ChannelType.text,
            discord.ChannelType.voice,
            discord.ChannelType.stage_voice,
            discord.ChannelType.forum,
            discord.ChannelType.media
        ):
            await interaction.response.send_message(
                "This command can only be used in a server channel.",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
            return
    
        log_channel_id = 1341072425248620629 # SET ID HERe
        log_channel = self.bot.get_channel(log_channel_id)

        # Log channel check
        if log_channel is None:
            await interaction.response.send_message(
                "I didn't find the channel :(",
                ephemeral=True, # Only the user sees this error message
                allowed_mentions=no_mentions
            )
            return

        # Deletion reason
        if reason is None or reason.strip() == "":
            reason_display = "No reason provided."
            deletion_reason_audit_log = "No reason" # AUDIT LOG
        else:
            reason_display = reason.strip()
            deletion_reason_audit_log = reason.strip()

        current_channel = interaction.channel
        channel_name = getattr(current_channel, "name", str(current_channel))
        channel_id = current_channel.id
        user_display_name = interaction.user.display_name
        user_id = interaction.user.id

        # Say it in the channel.
        await interaction.response.send_message(
            f"I love mods hi the delete thing is going to work (3s)",
            allowed_mentions=no_mentions # also no pings (to be safe fuck yall green roles) IF SOMEONE NAMES THEMSELF @EVERYONE THEYRE GETTING SKINNED!
        )

        # msg content
        log_message_content = (
            f"# Channel deletion!!!\n"
            f"**Channel Name:** `#{channel_name}` (ID: `{channel_id}`)\n"
            f"**Who did it:** {user_display_name} (ID: `{user_id}`)\n"
            f"**Reason:** {reason_display}"
        )
        await asyncio.sleep(3) # 
        try:
            # delete
            if isinstance(current_channel, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.ForumChannel, discord.CategoryChannel)):
                await current_channel.delete(reason=f"Deny-Delete command by {user_display_name} (ID: {user_id}). Reason: {deletion_reason_audit_log}")
            else:
                await interaction.followup.send(
                    "Can't delete :(",
                    ephemeral=True,
                    allowed_mentions=no_mentions
                )
                print(f"Tried to delete unsupported channel type: {type(current_channel).__name__} (ID: {channel_id})")
        except discord.Forbidden:
            # If no perms stuff
            await interaction.followup.send(
                "No perms to delete :(",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
            print(f"I lacks permissions to delete channel {channel_name} (ID: {channel_id})!!!!!!")
        except discord.HTTPException as e:
            # HTTP ERRORS
            await interaction.followup.send(
                f"Error deleting channel: {e}",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
            print(f"Error deleting channel {channel_name} (ID: {channel_id}): {e}")


        await asyncio.sleep(1) # 
        try:
            # check if can msg
            if isinstance(log_channel, (discord.TextChannel, discord.Thread)):
                await log_channel.send(log_message_content, allowed_mentions=no_mentions) # also no pings
            else:
                print(f"Error: Log channel {log_channel_id} cant send - (type: {type(log_channel).__name__})")
                await interaction.followup.send(
                    "Error: Cant send a msg in log channel (likely missing perms OR not a text channel)",
                    ephemeral=True,
                    allowed_mentions=no_mentions
                )
        except discord.Forbidden:
            print(f"Error: Bot lacks permissions to send messages in log channel {log_channel_id}")
            await interaction.followup.send(
                "Cant send log due to perms :(",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
        except discord.HTTPException as e:
            print(f"Error sending log message: {e}")
            await interaction.followup.send(
                f"An error occurred while sending the log message: {e}",
                ephemeral=True,
                allowed_mentions=no_mentions
            )


     

    # Error handler (copied i love github and stackoverflow RAHHHHHHHHHHHHHHHHHHHHHH)
    @deny_delete.error
    async def deny_delete_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        # no pings AGAIN
        no_mentions = discord.AllowedMentions.none()

        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You need the 'Manage Channels' permission to use this command.",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
        elif isinstance(error, app_commands.NoPrivateMessage): # mmmmmmmmmmmmmmmmmmmmm
            await interaction.response.send_message(
                "This command cannot be used in private messages.",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
        else:
            await interaction.response.send_message(
                f"An unexpected error occurred: {error}",
                ephemeral=True,
                allowed_mentions=no_mentions
            )
            print(f"Unhandled error in deny-delete command: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(DenyDeleteCog(bot))
