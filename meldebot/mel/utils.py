from functools import wraps
import telegram

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                     action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

def get_username(telegram_message):
    return telegram_message.username or telegram_message.full_name