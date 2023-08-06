import json
import logging
from urllib import request

from arkive.core.message import RestMessage

logger = logging.getLogger(__name__)


def send_request(message: RestMessage) -> dict:
    logger.debug(f'Sending message for {message.scope}.')
    response = request.urlopen(message.encode_url())
    data = json.load(response)
    logger.debug(f'Received response for {message.scope} with status {data["result"]}.')
    return data
