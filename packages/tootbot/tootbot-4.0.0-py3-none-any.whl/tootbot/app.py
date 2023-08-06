"""This module contains the main logic for tootbot."""
import sys
import time

from alive_progress import alive_bar
from rich import print as rprint

from tootbot import __version__
from tootbot.collect import LinkedMediaHelper
from tootbot.collect import RedditHelper
from tootbot.control import Configuration
from tootbot.monitoring import HealthChecks
from tootbot.publish import MastodonPublisher


def main() -> None:
    """Main / Overall Logic of tootbot.

    :param: None
    :return: None
    """
    config = Configuration()

    rprint(f"Welcome to Tootbot ({__version__})")

    title = "Setting up shop "
    with alive_bar(
        title=f"{title:.<60}",
        manual=True,
        enrich_print=False,
    ) as progress_bar:

        progress_bar.text = "Connecting to Mastodon instance ..."
        mastodon_publisher = MastodonPublisher(config=config)
        progress_bar(0.4120)  # pylint: disable=not-callable

        healthcheck = HealthChecks(config=config)
        progress_bar(0.4122)  # pylint: disable=not-callable

        reddit = RedditHelper(config=config)
        progress_bar(0.4130)  # pylint: disable=not-callable

        progress_bar.text = "Connecting to Imgur and Gfycat ..."
        media_helper = LinkedMediaHelper(config=config)
        progress_bar(1.0)  # pylint: disable=not-callable

    # Run the main script
    while True:
        if config.health.enabled:
            healthcheck.check_start()

        reddit_posts = {}
        for subreddit in config.subreddits:
            reddit_posts[subreddit.tags] = reddit.get_reddit_posts(
                subreddit.name, limit=config.reddit.post_limit
            )
        mastodon_publisher.make_post(reddit_posts, reddit, media_helper)

        if config.health.enabled:
            healthcheck.check_ok()

        if config.bot.run_once_only:
            config.bot.logger.debug(
                "Exiting because RunOnceOnly is set to %s", config.bot.run_once_only
            )
            sys.exit(0)

        sleep_time = config.bot.delay_between_posts

        # Determine how long to sleep before posting again
        if (
            config.mastodon_config.throttling_enabled
            and config.mastodon_config.number_of_errors
        ):
            sleep_time = (
                config.bot.delay_between_posts * config.mastodon_config.number_of_errors
            )
            if sleep_time > config.mastodon_config.throttling_max_delay:
                sleep_time = config.mastodon_config.throttling_max_delay

        config.bot.logger.debug("Sleeping for %s seconds", sleep_time)

        bar_title = "Sleeping before posting next toot"
        with alive_bar(
            title=f"{bar_title:.<60}",
            total=sleep_time,
            enrich_print=False,
            stats=False,
            monitor="{count}/{total} seconds",
            elapsed=False,
        ) as progress_bar:
            for _i in range(sleep_time):
                time.sleep(1)
                progress_bar()  # pylint: disable=not-callable

        rprint(" ")
        config.bot.logger.debug("Restarting main process...")


if __name__ == "__main__":
    main()
