from typing import Optional

from nautilus_trader.config.nodes import TradingNodeConfig as NautilusTradingNodeConfig

from nacre.config.actors import ExposerConfig
from nacre.config.actors import PubSubConfig


class TradingNodeConfig(NautilusTradingNodeConfig):
    """
    Configuration for ``TradingNode`` instances.

    pubsub: PubSubConfig, optional
        The config for external msgbus pubsub
    exposer: ExposerConfig, optional
        The config for exposer
    """

    pubsub: Optional[PubSubConfig] = None
    exposer: Optional[ExposerConfig] = None
