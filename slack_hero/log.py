import math
import logging
import os
import traceback
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

CLIENT = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
DIVIDER_BLOCK = {"type": "divider"}

def post_to_slack_channel(channel_id, message, subject=None):
    if subject:
        subject = subject.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        subject = '*' + subject + '* \n'
    else:
        subject = ''
    title_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": subject
        }
    }

    logger = logging.getLogger(__name__)
    if message:
        try:
            message_blocks = []
            # https://api.slack.com/reference/block-kit/blocks#section
            # Maximum text for each section block is 3000, so we split our message into multiple sections
            split = 3000
            parts = range( math.ceil( len(message.encode('utf8') ) / split ) )
            for part in parts:
                start = 0 if part == 0 else split * part
                end = split if part == 0 else split * part + split
                detail_text = message[start:end]
                message_blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": detail_text
                        }
                    })
            full_message = subject + '\nn' + message
            print('one',full_message)
            print([
                    DIVIDER_BLOCK,
                    title_block,
                    *message_blocks,
                ])
            result = CLIENT.chat_postMessage(
                channel=channel_id,
                text=full_message,
                blocks=[
                    DIVIDER_BLOCK,
                    title_block,
                    *message_blocks,
                ]
            )
            logger.warning("Result: {}".format(str(result)))
        except SlackApiError as error:
            if os.environ.get('DEBUG'):
                logger.warning("{}".format(message))
            else:
                logger.warning("Error posting to slack: {} \n Debug info below \n{}".format(str(error), message))

class SlackExceptionHandler(logging.Handler):
    def __init__(self, **kwargs):
        logging.Handler.__init__(self)

    def emit(self, record):
        subject = f'{record.levelname}: {record.getMessage()}'
        if record.exc_info:
            errType, errValue, errTraceback = record.exc_info
            message = "".join(traceback.format_exception(errType, errValue, errTraceback))
        else:
            message = ''
        post_to_slack_channel(os.environ.get('SLACK_CHANNEL', '#test-exceptions'), message, subject)
