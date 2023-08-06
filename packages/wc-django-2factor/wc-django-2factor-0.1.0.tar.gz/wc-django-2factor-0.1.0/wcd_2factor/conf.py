from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING

from px_settings.contrib.django import settings as s

if TYPE_CHECKING:
    from .sender import SenderConfig


__all__ = 'Settings', 'settings',


@s('WCD_2FACTOR')
@dataclass
class Settings:
    """
    Example:

    ```python
    WCD_2FACTOR = {
        'SENDERS': {
            'default': {
                'verbose_name': 'Phone sender',
                'backend': 'some.method.path.to.Backend',
                'options': {
                    'SECRET: 'SECRET',
                },
            },
        },
        'DEFAULT_SENDER': 'default',
        'CONFIRM_CODE_GENERATOR': 'wcd_2factor.services.confirmer.make_confirmation_code',
    }
    ```
    """
    SENDERS: Dict[str, 'SenderConfig'] = field(default_factory=dict)
    DEFAULT_SENDER: str = 'default'
    CACHE: str = 'default'
    CONFIRM_CODE_GENERATOR: str = 'wcd_2factor.services.confirmer.make_confirmation_code'

    def get_sender_choices(self):
        return [
            (key, config.get('verbose_name', key))
            for key, config in self.SENDERS.items()
        ]


settings = Settings()
