from telegram.ext import CommandHandler


def get_question(args):
    question = "Mel?"
    if args is not None and args:
        more_question = ' '.join(args)
        question = '{}\n{}'.format(more_question, question)
    return question

def start_poll(bot, update, args):
    update.message.reply_text('WIP!\n'+get_question(args=args))

poll_handler = CommandHandler('poll', start_poll, pass_args=True)