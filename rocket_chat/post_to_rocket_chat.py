#!/bin/env python
# GT4Py - GridTools Framework
#
# Copyright (c) 2014-2024, ETH Zurich
# All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

"""This script reports the result of the ReFrame test to the Rocket-Chat."""

from typing import Any, Optional

import argparse
import os
import sys
from pathlib import Path

from rocketchat_API.rocketchat import RocketChat


SERVER_URL: str = "https://chat.csc.fi"
"""The URL where the Rocket-Chat server is running on."""


def main(
    API_token: Optional[str],
    room_id: str,
    user_id: str,
    message_file: Path,
) -> int:
    """Post the content of `message_file` on the Rocket-Chat.

    Args:
        API_token: The token that should be used to authenticate the posting.
            If not given it will be read from the variable `ROCKET_CHAT_TOKEN`.
        room_id: The room/channel where we should do the posting.
        user_id: ID of the user that should do the post.
        message_file: The file containing the body of the message.
    """
    assert len(room_id) != 0
    assert len(user_id) != 0

    if not message_file.exists():
        raise FileNotFoundError(
            f"The file containing the message's body, '{message_file}', could not be located."
        )

    if not API_token:
        try:
            API_token = os.environ.get("ROCKET_CHAT_TOKEN")
        except KeyError:
            raise RuntimeError(
                "The API token was not given and `ROCKET_CHAT_TOKEN` was not set."
            ) from None

    with open(message_file, "rt") as F:
        message_body = "".join(F.readlines())

    rocket = RocketChat(
        user_id=user_id,
        auth_token=API_token,
        server_url=SERVER_URL,
    )

    result: dict[str, Any] = rocket.chat_post_message(
        message_body,
        room_id=room_id,
    ).json()

    if result.get("success", False):
        return 0
    else:
        raise RuntimeError(
            "Failed to successfully submit the post to {SERVER_URL} with error: {result.get('error', 'Unknown error')}"
        )


if __name__ == "__main__":
    args = argparse.ArgumentParser(prog="run_reporter.py")

    args.add_argument(
        "--api-token",
        dest="API_token",
        help="The API token that should be used for authentification, if not given read from `ROCKET_CHAT_TOKEN`.",
        type=str,
    )
    args.add_argument(
        "--message-file",
        dest="message_file",
        help="File containing the body of the post that should be made.",
        type=Path,
    )
    args.add_argument(
        "--room", "--room-id",
        dest="room_id",
        help="The ID of the room where we the post should be done.",
        type=str,
    )
    args.add_argument(
        "--user", "--user-id",
        dest="user_id",
        help="The ID of the user that does the posting.",
        type=str,
    )

    parsed_args = args.parse_args()

    sys.exit(
        main(
            API_token=parsed_args.API_token,
            room_id=parsed_args.room_id,
            user_id=parsed_args.user_id,
            message_file=parsed_args.message_file,
        )
    )
