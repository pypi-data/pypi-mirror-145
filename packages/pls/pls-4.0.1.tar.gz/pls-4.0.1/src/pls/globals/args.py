import argparse
import logging

from pls.config import prefs


logger = logging.getLogger(__name__)


class UpdatableNamespace(argparse.Namespace):
    """
    Extends ``argparse.Namespace`` to add support for overwriting attributes from
    another ``argparse.Namespace`` instance.
    """

    def update(self, more: argparse.Namespace):
        """
        Overwrite own attributes with attributes from another namespace.

        :param more: the namespace from which to read the attributes
        """

        logger.info("Updating namespace")

        logger.debug(f"Current: {self}")
        logger.debug(f"Incoming: {more}")

        for key, val in vars(more).items():
            if key not in self or val is not None:
                if val == "default":
                    val = getattr(prefs.internal_prefs, key, None)
                setattr(self, key, val)

        logger.debug(f"Result: {self}")


args: argparse.Namespace = UpdatableNamespace()
"""the arguments read from the terminal and parsed from prefs"""
