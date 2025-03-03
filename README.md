# lumi-reframe-tests
LUMI Reframe Test Suite

# Wrapper
You can use ReFrame directly, i.e. by writing `reframe`, as an alternative you can also use the `start_reframe_tests.sh` wrapper.
This script accepts the same argument as `reframe` and will start the specified tests.
However, it will also report the results of the tests back by making a post in the Rocket-Chat.
The wrapper also accepts the `--no-rocket-chat-post` argument, which will instruct the wrapper to not make a post.

The message the wrapper posts if the tests are successful is read from `rocket_chat/success.md` and from `rocket_chat/failure.md` if they fail.


### Dependencies
To use the wrapper and perform the post the following conditions have to be meet.
- You must specify the `USER_ID` and `ROOM_ID` in the wrapper.
    These variables are needed to make a post.
- You must export the `ROCKET_CHAT_TOKEN` variable, which is the API token that allows the user, i.e. `USER_ID`, to authenticate itself.
- You must install reframe, i.e. the `reframe` command must be available.
- You must have installed the [`rocketchat_API`](https://github.com/jadolg/rocketchat_API).



