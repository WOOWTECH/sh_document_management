# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
# BUG-002 Fix: Auto-detect public URLs for document sharing

import ipaddress
import logging
from urllib.parse import urlparse
from odoo import models, api

_logger = logging.getLogger(__name__)


class IrConfigParameterInherit(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def set_param(self, key, value):
        """Override to detect public URL when web.base.url changes."""
        result = super().set_param(key, value)

        # ONLY process web.base.url changes (not our own parameter to avoid recursion)
        if key == 'web.base.url' and value:
            is_public = self._is_public_url(value)
            _logger.info(
                f"web.base.url changed to: {value} (public: {is_public})"
            )

            if is_public:
                # Use super() call to bypass our override and prevent recursion
                old_public = super(IrConfigParameterInherit, self).sudo().search([
                    ('key', '=', 'sh_document_management.public_base_url')
                ], limit=1).value

                super(IrConfigParameterInherit, self).sudo().set_param(
                    'sh_document_management.public_base_url',
                    value
                )

                _logger.info(
                    f"Updated sh_document_management.public_base_url: "
                    f"{old_public} -> {value}"
                )

        return result

    def write(self, vals):
        """Override to detect public URL when web.base.url is updated."""
        result = super().write(vals)

        if 'value' in vals:
            # Find web.base.url record(s) in this recordset
            web_base_params = self.filtered(lambda r: r.key == 'web.base.url')
            if web_base_params and vals['value']:
                is_public = self._is_public_url(vals['value'])
                _logger.info(
                    f"web.base.url updated to: {vals['value']} (public: {is_public})"
                )

                if is_public:
                    # Use super() to avoid recursion
                    super(IrConfigParameterInherit, self).sudo().set_param(
                        'sh_document_management.public_base_url',
                        vals['value']
                    )

        return result

    @api.model
    def _is_public_url(self, url):
        """
        Returns True if URL uses a public domain/IP.
        Returns False for private IPs (192.168.x.x, 10.x.x.x, etc.), localhost, or invalid URLs.
        """
        if not url:
            return False

        try:
            parsed = urlparse(url)
            host = parsed.hostname

            if not host:
                return False

            # Check for localhost
            if host in ('localhost', '127.0.0.1', '::1'):
                return False

            # Check for local domain suffixes
            local_suffixes = (
                '.local', '.localhost', '.internal', '.lan', '.home',
                '.intranet', '.corp', '.private', '.test', '.example'
            )
            if any(host.lower().endswith(suffix) for suffix in local_suffixes):
                return False

            # Check if it's an IP address
            try:
                ip = ipaddress.ip_address(host)
                # Private IPs: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
                # Also reject loopback, link-local, multicast
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
                    return False
                return True
            except ValueError:
                # Not an IP address - check if it looks like a domain
                # Domain must have at least one dot and valid characters
                if '.' in host and all(c.isalnum() or c in '.-' for c in host):
                    return True
                return False

        except Exception as e:
            _logger.warning(f"Invalid URL in _is_public_url: {url} - {e}")
            return False
