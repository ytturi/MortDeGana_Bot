from functools import wraps
import telegram

from meldebot.mel.conf import get_debug_enabled


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


def remove_command_message(func):
    """Removes the message that triggered the handler."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        if get_debug_enabled():
            return func(update, context, *args, **kwargs)
        return_value = func(update, context, *args, **kwargs)
        # Try to remove the original message
        try:
            update.effective_message.delete()
        except:
            # It raises an exception if
            # - it's already removed
            # - it doesn't have permissions
            # But we don't care
            pass
        return return_value

    return command_func


def get_username(telegram_message):
    return telegram_message.username or telegram_message.full_name
