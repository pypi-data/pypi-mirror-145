#!/usr/bin/env python3

import argparse
import json
import logging
import secrets
import signal
import sys
from subprocess import PIPE, Popen
from time import sleep

import boto3
from botocore.exceptions import ClientError
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

LOGGER = logging.getLogger(__name__)


class SNSTopicListener:
    def __init__(self, account_id, topic, debug=False, sig=signal.SIGINT):
        self.sig = sig
        self.topic = topic
        self.account_id = account_id
        self.debug = debug
        self.create_queue()
        self.subscribe()

    def create_queue(self):
        self.sns_client = boto3.client("sns")
        response = self.sns_client.list_topics()
        arns = [x["TopicArn"] for x in response["Topics"]]

        if not self.topic:
            topic_completer = WordCompleter([x.split(":")[-1] for x in arns])
            self.topic = prompt("Choose topic: ", completer=topic_completer)

        matches = [arn for arn in arns if self.topic in arn]

        self.topic_arn = matches[0]

        rando_hex = secrets.token_hex(5)
        sqs_queue_name = f"sns-listener_{self.topic}_{rando_hex}"
        email = f"{sqs_queue_name}@honnecke.us"

        # Get the service resource
        sqs_client = boto3.resource("sqs")

        # Create the queue. This returns an SQS.Queue instance
        self.sqs_queue = sqs_client.create_queue(
            QueueName=sqs_queue_name, Attributes={"DelaySeconds": "5"}
        )

        self.sqs_queue_arn = self.sqs_queue.attributes["QueueArn"]
        if ":sqs." in self.sqs_queue_arn:
            self.sqs_queue_arn = self.sqs_queue_arn.replace(":sqs.", ":")

        formattend_policy = json.dumps(
            {
                "Version": "2008-10-17",
                "Id": f"__auto_policy_{rando_hex}",
                "Statement": [
                    {
                        "Sid": "__owner_statement",
                        "Effect": "Allow",
                        "Principal": {"AWS": f"arn:aws:iam::{self.account_id}:root"},
                        "Action": "SQS:*",
                        "Resource": self.sqs_queue_arn,
                    },
                    {
                        "Sid": "topic-subscription-arn:" + self.topic_arn,
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "SQS:SendMessage",
                        "Resource": self.sqs_queue_arn,
                        "Condition": {"ArnLike": {"aws:SourceArn": self.topic_arn}},
                    },
                ],
            }
        )
        # breakpoint()
        self.sqs_queue.set_attributes(Attributes={"Policy": formattend_policy})

    def subscribe(self):
        # Subscribe SQS queue to SNS
        return self.sns_client.subscribe(
            TopicArn=self.topic_arn, Protocol="sqs", Endpoint=self.sqs_queue_arn
        )

    def __enter__(self):

        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.remove_queue()
        self.release()

    def release(self):

        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)

        self.released = True

        return True

    def remove_queue(self):
        try:
            self.sqs_queue.delete()
            print(f"Deleted queue with URL {self.sqs_queue.url}.")
            LOGGER.info("Deleted queue with URL=%s.", self.sqs_queue.url)
        except ClientError as error:
            LOGGER.exception("Couldn't delete queue with URL=%s!", self.sqs_queue.url)
            raise error

    def listen(self):
        messages = self.sqs_queue.receive_messages(
            AttributeNames=["All"],
            MessageAttributeNames=["All"],
            VisibilityTimeout=15,
            WaitTimeSeconds=1,
            MaxNumberOfMessages=1,
        )
        if messages:
            m = messages[0]  # pylint: disable=invalid-name

            if self.debug:
                print("Dropping into debugger for inspection")
                print("Local message variable is 'm'")
                print("PDB commands: 'c' to continue, 'exit()' to exit")
                breakpoint()
            else:
                print(f"Recieved message, {m.body}")

            m.delete()

        print("Listening...")
        sleep(1)


def parse_args():
    """
    Extract the CLI arguments from argparse
    """
    _parser = argparse.ArgumentParser(description="Listen to an SNS topic")

    _parser.add_argument(
        "-p",
        "--profile",
        help="AWS profile name",
    )
    _parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Drop into debugger to inspect message",
    )
    _parser.add_argument(
        "-t",
        "--topic",
        help="SNS topic name",
        required=False,
    )
    return _parser.parse_args()


def get_caller_identity():
    if identity := aws_cli_execute(["sts", "get-caller-identity"]):
        return json.loads(identity)
    return None


def get_config_identity():
    return aws_cli_execute(["configure", "list"]).split("\n")


def get_available_profiles():
    return aws_cli_execute(["configure", "list-profiles"]).split("\n")


def is_logged_in() -> bool:
    """
    Check to see if the user is logged in to AWS
    """
    return bool(get_caller_identity())


def get_account_id() -> bool:
    return get_caller_identity().get("Account")


def get_profile():
    profiles = get_available_profiles()
    profile_completer = WordCompleter(profiles)
    return prompt(
        "Profile was not passed, choose a profile: ", completer=profile_completer
    )


def cli_execute(command):
    with Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        output, err = process.communicate(
            b"input data that is passed to subprocess' stdin"
        )
        if err:
            print(err.decode("utf-8"))

    return output.decode("utf-8")


def aws_cli_execute(command):
    command.insert(0, "aws")
    return cli_execute(command)


def run():
    args = parse_args()

    if not is_logged_in():
        print("Please log in to AWS cli")
        sys.exit(1)

    if not args.profile:
        args.profile = get_profile()

    boto3.setup_default_session(profile_name=args.profile)
    account_id = get_account_id()

    with SNSTopicListener(account_id, args.topic, args.debug) as dolores:
        while not dolores.released:
            dolores.listen()


if __name__ == "__main__":
    run()
