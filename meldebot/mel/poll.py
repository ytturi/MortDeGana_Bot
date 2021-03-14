###############################################################################
# Project: Mort de Gana Bot
# Authors:
# - Ytturi
# - gdalmau
# Descr: Polling manager
# Commands:
# - Poll: Send a poll with a specified message. Usage: `/poll {message}`
###############################################################################
from __future__ import annotations
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice, randint
from logging import getLogger
from sqlalchemy import bindparam, select

# Self imports
from meldebot.mel.gif import get_gifs
from meldebot.mel.utils import send_typing_action, remove_command_message, get_username
from meldebot.mel.conf import get_database

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext
    from meldebot.database import Database

logger = getLogger(__name__)

# Mort de Gana POLL MANAGER

# MOTO QUOTES
MOTO_QUOTE = [
    f"Fa {randint(2,30)} anys plovia",
    f"Tinc hora a la pelu que nomes hi vaig {randint(1,20)} cops per setmana",
    f"Vaig al gym, la idea es anarhi {randint(1,20)} cops per setmana",
    "Aquest dia justament vaig a donar sang",
    "Casum l'olla! Tinc un dinar familiar",
    "Demà haig d'anar a passar la itv",
    "El metge m'ha dit que no puc menjar aliments rics en sodi",
    "Esque em guardo dies de vacances",
    "Esque se m'ha punxat la roda de la bici estàtica i l'he de canviar",
    "Esque vai demanar un paquet i crec que m'arribarà llavors",
    "Esque fa molt sol i no tinc crema",
    "Esque he d'anar a treure la marmota a passejar",
    "Estic esperant a que el Jefe em doni el contracte que m'ha dit que ara me'l porta",
    "Estic esperant la corda i tamboret que m'he demanat a amazon",
    "He quedat per fer una muntanya",
    "Jo vindira, però es que se m'ha espatllat el GPS del mòbil",
    "Jo vindria, però m'agrada fer motos",
    "Jo vindria, però es que s'em morirà el peix que vaig a comprar ara",
    "Justament aquest dia he quedat per jugar a arrancar cebes"
    "M'he endescuidat de regar el cactus de gisce",
    "Mha semblat veure una gota a la carretera",
    "No puc venir pk la dona m'ha dit que anes a la platja de palafrugell i em quedés un parell d'hores sota l'aigua",
    "No puc venir que he d'afegir excuses de moto al bot",
    "Plou i fa sol, em quedo a casa sol",
    "Se m'ha mort el PC i li fem un funeral. Tenia una 3080ti",
    "Se m'ha mort la PS5 i li fem un funeral. Poques que n'hi han...",
    "Soc un mort de gana",
    "Tinc el rellotge en format 24h",
    "Tinc un conegut que fa casi un any que no veig que té corona, així que faig quarentena per si de cas.",
    "Tu que m'acaben de trucar que d'aqui 20min anem a fer una implantació i no sé quan tornaré.",
    "Volia venir pro no soy 1000itar",
    "Volia venir pro no soy 1000itante",
    "Volia venir pro no soy 100tifiko",
]


# POLL KEYBOARD
POLL_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("MEL", callback_data="vote MEL"),
            InlineKeyboardButton("MEL + 1", callback_data="vote MEL+1"),
            InlineKeyboardButton("MEL - 1", callback_data="vote MEL-1"),
        ],
        [
            InlineKeyboardButton("MOTO", callback_data="vote MOTO"),
        ],
    ]
)

# POLL START


def get_question(extra_text: str) -> str:
    question = "Mel o no?\n"
    if extra_text:
        question = "{}\n{}".format(extra_text, question)
    return question


def get_answers(status: Optional[List[str]] = None) -> str:
    if status is None:
        status = ["", ""]
    answer = "MEL!\n{}- {}\nMOTO!\n{}- {}".format(
        recount_result(status[0]),
        status[0],
        recount_result(status[1]),
        status[1],
    )
    return answer


def get_moto_quote() -> str:
    """Generate a random text for motos

    Returns:
        str: Moto quote
    """
    return choice(MOTO_QUOTE)


@send_typing_action
@remove_command_message
def start_poll(update: Update, context: CallbackContext) -> None:
    logger.info("Handling newpoll")
    text = "{}\n{}".format(
        get_question(extra_text=" ".join(context.args)), get_answers()
    )
    message = update.message.reply_text(text, reply_markup=POLL_KEYBOARD, quote=False)


POLL_START_HANDLER = CommandHandler("poll", start_poll, pass_args=True)


# POLL VOTE HANDLER


def result_user_votes(result):
    break_idx = False
    for idx, char in enumerate(result):
        if char == "-":
            break_idx = idx
            break
        if char == "@":
            # If there is no result part and we reach a username
            break
    if break_idx is False and result:
        return result.split(",")
    break_idx += 1
    votes = result[break_idx:].strip()
    if votes:
        return votes.split(",")
    else:
        return []


def recount_result(result):
    """Parse the result line and count the votes"""
    user_votes = result_user_votes(result)
    total = 0
    for vote in user_votes:
        if not vote:
            break
        total += 1
        if "+" in vote:
            total += int(vote[vote.index("+") + 1 :])
    return total


def insert_user_in_result(results, result_idx, user, extra=False):
    """
    Parse the result line and add the user and any extras.
      If the user is present in the other results string, remove it.
    """

    def search_user_vote(arr, user):
        user_vote_idx = False
        for idx, vote in enumerate(arr):
            if user in vote:
                user_vote_idx = idx
        return user_vote_idx

    def get_user_extra_vote(arr, user):
        idx = search_user_vote(arr, user)  # Search vote
        if idx is False:
            return 0
        vote = arr[idx][(len(user) + 2) :]  # Remove username from vote
        vote.strip()
        return int(vote) if vote else 0  # If any vote, parse to int

    # Init vote text
    text = "@{}".format(user)

    # Update results
    votes = result_user_votes(results[result_idx])

    # Find last vote (if any)
    user_vote_idx = search_user_vote(votes, user)

    if user_vote_idx is not False:
        # IF exists
        if extra:
            # If extra, update it
            extra = extra + get_user_extra_vote(votes, user)
            if extra and extra > 0:  # Can't set lower than 0
                text += "+{}".format(extra)
        votes[user_vote_idx] = text
        results[result_idx] = ",".join(votes)  # UPDATE

    else:
        # IF not exists, ADD the new vote
        # IF extra, add it
        if extra and extra > 0:  # Can't set lower than 0
            text += "+{}".format(extra)
        votes.append(text)
        votes = sorted(votes)  # SORT
        results[result_idx] = ",".join(votes)  # UPDATE

    # Clean other results and DEL old vote (if any)
    other_idx = 0 if result_idx else 1
    votes = result_user_votes(results[other_idx])
    user_vote_idx = search_user_vote(votes, user)
    if user_vote_idx is not False:
        del votes[user_vote_idx]
    results[other_idx] = ",".join(votes)  # UPDATE
    return results


def update_poll_message(text, user, query):
    question = text.split("\n")[:-4]
    results = text.split("\n")[-3:]
    results = [results[0], results[-1]]
    # DATA="vote [MEL|MOTO|MEL+1|MEL-1]"
    vote = query.data[5:]
    if "MEL" in vote:
        extra = int(vote[3:]) if vote[3:] else 0
        results = insert_user_in_result(results, 0, user=user, extra=extra)
    else:
        results = insert_user_in_result(results, 1, user=user)

    question.append(get_answers(results))
    return "\n".join(question)


def vote_poll(update: Update, context: CallbackContext) -> None:
    logger.info("Handling votepoll")
    username = get_username(update.effective_user)

    # Use old method by default
    if not get_database().enabled:
        message_text = update_poll_message(
            text=update.effective_message.text,
            user=username,
            query=update.callback_query,
        )

    # If database is enabled, use the new method
    else:
        message_text = new_update_poll_message(
            group_id=update.effective_message.chat_id,
            poll_id=update.effective_message.message_id,
            username=username,
            old_text=update.effective_message.text,
            query_data=update.callback_query.data,
        )

    if message_text == update.effective_message.text:
        return

    update.effective_message.edit_text(text=message_text, reply_markup=POLL_KEYBOARD)
    if "MOTO" in update.callback_query.data:
        update.effective_message.reply_animation(
            get_gifs("moto"), caption=f"{username}: {get_moto_quote()}", quote=True
        )


def new_update_poll_message(
    group_id: int,
    poll_id: int,
    username: str,
    old_text: str,
    query_data: str,
) -> str:
    """
    Generate the new text for the poll message and update the database

    Args:
        poll_id (int): Telegram's `message_id` for the poll
        username (str): Username of the user interacting with the poll
        old_text (str): Old message text
        query_data (str): Vote query data (Text from the pressed button)

    Returns:
        str: Updated poll text message
    """

    # Query data contains a string with the command sent when pressing
    # the button with the format:
    #
    #   "vote [MEL|MOTO|MEL+1|MEL-1]"
    #
    # Substracting the first 5 characters ("vote ") results in the
    # current vote action, which is one of:
    # - MEL
    # - MOTO
    # - MEL+1
    # - MEL-1
    vote_action = query_data[5:]

    handle_vote(poll_id, username, vote_action)

    votes = get_all_votes(poll_id)
    return build_new_message(old_text, votes)


def handle_vote(group_id: int, poll_id: int, username: str, vote_action: str) -> None:
    """
    Update the database according to the vote action
    for the effective user in the poll message

    Args:
        poll_id (int): Telegram's `message_id` for the poll
        username (str): Username of the user interacting with the poll
        vote_action (str): [description]
    """

    # Check for existing vote for this user:
    existing_vote = get_existing_vote(poll_id, username)
    vote_value: int

    # Possible actions:
    # - `MOTO`: set the vote to 0
    if vote_action == "MOTO":
        vote_value = 0

    # - `MEL`: set the vote to 1
    elif vote_action == "MEL":
        vote_value = 1

    # - `MEL+1`: Add 1 to the current vote
    elif vote_action == "MEL+1":
        if existing_vote is None:
            vote_value = 2

        else:
            vote_value = 2 if existing_vote < 2 else existing_vote + 1

    # - `MEL-1`: Substract 1 to the current vote (Can't be less than 1)
    elif vote_action == "MEL-1":
        if existing_vote is None:
            vote_value = 1

        else:
            vote_value = 1 if existing_vote < 2 else existing_vote - 1

    else:
        raise Exception(f"Unkown vote action {vote_action}")

    if existing_vote is None:
        insert_vote(group_id, poll_id, username, vote_value)

    else:
        update_vote(poll_id, username, vote_value)


def get_existing_vote(poll_id: int, username: str) -> Optional[int]:
    """
    Query the database to get the current vote for the user if it exists.

    Args:
        poll_id (int): Telegram's `message_id` for the poll
        username (str): Username of the user interacting with the poll

    Returns:
        int: [description]
    """

    postgres: Database = get_database()

    select_query = select([postgres.motos_counter.c.vote]).where(
        (postgres.motos_counter.c.poll_id == poll_id)
        & (postgres.motos_counter.c.username == bindparam("username_"))
    )
    # We only expect one row to match
    results = postgres.engine.execute(select_query, username_=username).first()

    if results is None:
        return None

    else:
        return results["vote"]


def insert_vote(group_id: int, poll_id: int, username: str, vote: int) -> None:
    """
    Insert a new vote into the database

    Args:
        poll_id (int): Telegram's `message_id` for the poll
        username (str): Username of the user interacting with the poll
        vote (int): New user vote
    """
    from datetime import datetime

    postgres: Database = get_database()

    insert_values = {
        "group_id": group_id,
        "poll_id": poll_id,
        "username": username,
        "vote": vote,
        # TODO: Move the date to PostgreSQL
        "date": datetime.now(),
    }

    insert_query = postgres.motos_counter.insert().values(insert_values)
    postgres.engine.execute(insert_query)


def update_vote(poll_id: int, username: str, vote: int) -> None:
    """
    Insert a new vote into the database

    Args:
        poll_id (int): Telegram's `message_id` for the poll
        username (str): Username of the user interacting with the poll
        vote (int): New user vote
    """
    from datetime import datetime

    postgres: Database = get_database()

    update_values = {
        "vote": vote,
        # TODO: Move the date to PostgreSQL
        "date": datetime.now(),
    }

    update_query = (
        postgres.motos_counter.update()
        .values(update_values)
        .where(
            (postgres.motos_counter.c.poll_id == poll_id)
            & (postgres.motos_counter.c.username == bindparam("username_"))
        )
    )
    postgres.engine.execute(update_query, username_=username)


def get_all_votes(poll_id: int) -> List[Tuple[str, int]]:
    """
    Get all votes for the current poll_id that are stored in the database

    Args:
        poll_id (int): Telegram's `message_id` for the poll

    Returns:
        List[Tuple[str, int]]: A list with the current votes in tuples (user, votes)
    """

    postgres: Database = get_database()

    select_query = (
        select([postgres.motos_counter.c.username, postgres.motos_counter.c.vote])
        .where(postgres.motos_counter.c.poll_id == poll_id)
        .order_by(postgres.motos_counter.c.vote, postgres.motos_counter.c.date)
    )

    results = postgres.engine.execute(select_query)

    return [(row["username"], row["vote"]) for row in results]


def build_new_message(old_message: str, votes: List[Tuple[str, int]]) -> str:
    """
    Build the new poll text message with the votes and the old message.

    Args:
        old_message (str): Old poll message.
            We use it to get the poll question
        votes (List[Tuple[str, int]]): All the votes in the database.
            Used to build the current answers.

    Returns:
        str: The new string to update the message
    """

    # This is a hack, but it's effective for now.
    # We know that the results are build as:
    #  "[Question]\n\nMEL\n<list of mel>\nMOTO\n<list of moto>"
    # Therefore we can split on '\n' and remove this part
    # by removing the last 4 '\n'
    question = "\n".join(old_message.split("\n")[:-4])

    mel_votes = [(f"@{user}", vote) for user, vote in votes if vote > 0]
    moto_votes = [f"@{user}" for user, vote in votes if vote == 0]

    total_mel = sum([vote for user, vote in mel_votes])
    total_moto = len([user for user in moto_votes])

    mel = f"MEL: {total_mel}\n"
    if total_mel > 0:
        mel += ", ".join(
            [f"{user}" if vote == 1 else f"{user}+{vote-1}" for user, vote in mel_votes]
        )

    else:
        mel += "-"

    moto = f"MOTO: {total_moto}\n"
    if total_moto > 0:
        moto += ", ".join(moto_votes)

    # Ensure we have a character in the row to preserve the same amount of '\n'
    else:
        moto += "-"

    return f"{question}\n{mel}\n{moto}"


POLL_VOTE_HANDLER = CallbackQueryHandler(vote_poll, pattern=r"^vote")


# HANDLERS to register


POLL_HANDLERS = [
    POLL_START_HANDLER,
    POLL_VOTE_HANDLER,
]
