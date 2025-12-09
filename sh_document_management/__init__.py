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
    config_param = env['ir.config_parameter']

    # Check if public_base_url already exists
    existing_public = IrConfig.get_param('sh_document_management.public_base_url')
    current_base = IrConfig.get_param('web.base.url')

    if existing_public:
        # FIX-006: Ensure existing public URL uses HTTPS
        https_url = config_param._ensure_https(existing_public)
        if https_url != existing_public:
            IrConfig.set_param('sh_document_management.public_base_url', https_url)
            _logger.info(
                f"Upgraded sh_document_management.public_base_url to HTTPS: "
                f"{existing_public} -> {https_url}"
            )
    elif current_base and config_param._is_public_url(current_base):
        # FIX-006: Force HTTPS for new public URLs
        https_url = config_param._ensure_https(current_base)
        IrConfig.set_param('sh_document_management.public_base_url', https_url)
        _logger.info(
            f"Initialized sh_document_management.public_base_url to {https_url}"
        )
    else:
        _logger.info(
            f"Current web.base.url ({current_base}) is not public. "
            f"Public URL will be set on first public login."
        )
