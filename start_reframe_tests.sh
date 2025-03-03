#!/bin/bash
# A wrapper arround the `reframe` command that also performs the posting to rocket chat.

# These are the configurations for makeing the post.
USER_ID=""
ROOM_ID=""

# This is the folder in which we started.
SCRIPT_FOLDER="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Ensure that reframe is installed.
if ! hash reframe >/dev/null 2>&1
then
	echo "The 'reframe' command was not found." >&2
	exit 2
fi

# Ensure that the Rocket-Chat API client is installed
if ! python -c 'import sys ; import rocketchat_API; sys.exit(0)' >/dev/null 2>&1
then
	echo "It seems that the 'rocketchat_API' Python package is not installed." >&2
	exit 2
fi

if [ -z "${USER_ID}" ] || [ -z "${ROOM_ID}" ]
then
	echo "You must set the 'USER_ID' and 'ROOM_ID' value in '$0'." >&2
	exit 3
fi
if [ -z "${ROCKET_CHAT_TOKEN}" ]
then
	echo "You must set the 'ROCKET_CHAT_TOKEN' environment variable." >&2
	exit 4
fi

# Look for the `--no-rocket-chat-post` flag to disable the posting.
#  Collect the other arguments into `REFRAME_ARGS`
DO_ROCKET_CHAT_POSTING=1
declare -a REFRAME_ARGS=()
for iARG in "$@"
do
	if [ "${iARG}" = "--no-rocket-chat-post" ]
	then
		DO_ROCKET_CHAT_POSTING=0
	else
		REFRAME_ARGS+=( "${iARG}" )
	fi
done

# Now call reframe with the arguments.
reframe "${REFRAME_ARGS[@]}"
REFRAME_STATUS="$?"

if [ "${DO_ROCKET_CHAT_POSTING}" -ne 0 ]
then
	if [ "${REFRAME_STATUS}" -eq 0 ]
	then
		MESSAGE_BODY="${SCRIPT_FOLDER}/rocket_chat/success.md"
	else
		MESSAGE_BODY="${SCRIPT_FOLDER}/rocket_chat/failure.md"
	fi

	python "${SCRIPT_FOLDER}/rocket_chat/post_to_rocket_chat.py" --user-id "${USER_ID}" --room-id "${ROOM_ID}" --message-file "${MESSAGE_BODY}"
fi

exit "${REFRAME_STATUS}"
