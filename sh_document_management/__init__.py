# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from . import models
from . import wizard
from . import controllers


def post_init_hook(env):
    """Initialize public_base_url after module installation."""
    import logging
    _logger = logging.getLogger(__name__)

    IrConfig = env['ir.config_parameter'].sudo()

    # Check if public_base_url already exists
    if not IrConfig.get_param('sh_document_management.public_base_url'):
        current_base = IrConfig.get_param('web.base.url')

        # Use inherited method to check if current URL is public
        config_param = env['ir.config_parameter']
        if current_base and config_param._is_public_url(current_base):
            IrConfig.set_param('sh_document_management.public_base_url', current_base)
            _logger.info(
                f"Initialized sh_document_management.public_base_url to {current_base}"
            )
        else:
            _logger.info(
                f"Current web.base.url ({current_base}) is not public. "
                f"Public URL will be set on first public login."
            )
