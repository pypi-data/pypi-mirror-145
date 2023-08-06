import datetime
import functools
import json
import os
import socket
import traceback
from typing import Sequence, Optional, Callable

import requests

import sfu_torch_lib.mlflow as mlflow
import sfu_torch_lib.parameters as parameters_lib


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def notify(
        function: Callable,
        webhook_url: str = os.environ['SLACK_URL'],
        user_ids: Optional[Sequence[str]] = None,
) -> Callable:
    """
    Executes a function and sends a Slack notification with the final status (successfully finished or
    crashed). Also sends a Slack notification before executing the function.
    Visit https://api.slack.com/incoming-webhooks#create_a_webhook for more details.
    Visit https://api.slack.com/methods/users.identity for more details.

    :param function: Function to annotate and execute.
    :param webhook_url: The webhook URL to your slack channel.
    :param user_ids: Optional user ids to notify.
    """
    if user_ids is None:
        user_ids = [os.environ['SLACK_USER']] if os.getenv('SLACK_USER') else []

    user_mentions = ', '.join(f'<@{user_id}>' for user_id in user_ids)

    parameters = '\n'.join(
        f'\t{key}: {value}'
        for key, value
        in parameters_lib.get_script_parameters(function, ignore_keyword_arguments=False).items()
    )

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        host_name = socket.gethostname()

        if 'RANK' in os.environ:
            master_process = (int(os.environ['RANK']) == 0)
            host_name += f' - RANK: {os.environ["RANK"]}'
        else:
            master_process = True

        if master_process:
            contents = [
                '*🎬 Your job has started*',
                f'Machine name: {host_name}',
                f'Starting time: {start_time.strftime(DATE_FORMAT)}',
                f'Parameters:\n{parameters}',
                f'User: {user_mentions}',
            ]

            message = {'text': '\n'.join(contents)}
            requests.post(webhook_url, json.dumps(message))

        try:
            value = function(*args, **kwargs)

            metrics = '\n'.join(
                f'\t{key}: {value}'
                for key, value
                in mlflow.get_metrics().items()
            )

            if master_process:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                contents = [
                    '*🎉 Your job is complete*',
                    f'Machine name: {host_name}',
                    f'Starting time: {start_time.strftime(DATE_FORMAT)}',
                    f'End date: {end_time.strftime(DATE_FORMAT)}',
                    f'Duration: {elapsed_time}',
                    f'Main call returned value: {value}',
                    f'Parameters:\n{parameters}',
                    f'Metrics:\n{metrics}',
                    f'User: {user_mentions}',
                ]

                message = {'text': '\n'.join(contents)}
                requests.post(webhook_url, json.dumps(message))

            return value

        except Exception as exception:
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            contents = [
                '*☠️ Your job has crashed*',
                f'Machine name: {host_name}',
                f'Starting time: {start_time.strftime(DATE_FORMAT)}',
                f'End date: {end_time.strftime(DATE_FORMAT)}',
                f'Duration: {elapsed_time}\n\n',
                f'Error:\n{exception}\n\n',
                f'Traceback:\n{traceback.format_exc()}',
                f'User: {user_mentions}',
            ]

            message = {'text': '\n'.join(contents)}
            requests.post(webhook_url, json.dumps(message))

            raise exception

    return wrapper
