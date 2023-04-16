import os

from dff.script import RESPONSE, TRANSITIONS, Message
from dff.messengers.telegram import PollingTelegramInterface
from dff.pipeline import Pipeline
from dff.script import GLOBAL, TRANSITIONS, RESPONSE, Context, Actor, Message
from dff.utils.testing.common import is_interactive_mode


from dialog_flow import script


interface = PollingTelegramInterface(token=os.getenv("TG_BOT_TOKEN", ""))

pipeline = Pipeline.from_script(
    script=script,  # Actor script object
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
    messenger_interface=interface,  # The interface can be passed as a pipeline argument.
)


def main():
    if not os.getenv("TG_BOT_TOKEN"):
        print("`TG_BOT_TOKEN` variable needs to be set to use TelegramInterface.")
    pipeline.run()


if __name__ == "__main__" and is_interactive_mode():  # prevent run during doc building
    main()