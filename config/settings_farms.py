"""Settings for the farms.afraviva.com Passenger app. Same codebase and
database as the main site — only the URLconf differs, so this domain serves
Farms hub content at its root instead of /farms/.
"""

from .settings import *  # noqa: F401,F403

ROOT_URLCONF = "config.urls_farms"
