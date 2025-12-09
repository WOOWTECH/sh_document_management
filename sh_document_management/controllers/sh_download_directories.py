# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import io
import logging
import zipfile
from odoo.http import request, content_disposition
from odoo import http, SUPERUSER_ID

logger = logging.getLogger(__name__)


class ShDocumentCustomerPortal(http.Controller):

    @http.route(['/attachment/download_directiries',], type='http', auth='public', website=False, csrf=False)
    def sh_download_directiries(self, list_ids='', access_token='', name='', **post):
        """Controller to download share document from click on the click to download button from the email"""
        if not list_ids or not access_token:
            return request.not_found()

        # Validate access token based on type
        if name == 'directory':
            record = request.env['document.directory'].sudo().browse(int(list_ids))
            if not record.exists() or record.sh_access_token != access_token:
                return request.not_found()
        elif name == 'document':
            record = request.env['ir.attachment'].sudo().browse(int(list_ids))
            if not record.exists() or record.access_token != access_token:
                return request.not_found()
        else:
            return request.not_found()
        stream = io.BytesIO()
        try:
            with zipfile.ZipFile(stream, 'w') as doc_zip:
                attachment = request.env['ir.attachment']
                domain = [('type', '!=', 'empty')]
                Name = None
                if name == 'directory':
                    domain.append(('directory_id.id', 'in', [list_ids]))
                    directory = request.env['document.directory']
                    directories = directory.sudo().search(
                        [('id', '=', list_ids or list_ids[0] or False)])
                    Name = directories.name

                if name == 'document':
                    domain.append(('id', 'in', [list_ids]))
                    directories = attachment.sudo().search(
                        [('id', '=', list_ids or list_ids[0] or False)])

                    Name = directories.name.split(".")
                    Name = Name[0]

                attachments = attachment.sudo().search(domain)

                for attached_document in attachments:
                    if attached_document.with_user(SUPERUSER_ID).type != 'binary':
                        continue
                    binary_stream = request.env['ir.binary'].with_user(SUPERUSER_ID)._get_stream_from(
                        attached_document, 'raw')
                    doc_zip.writestr(
                        binary_stream.download_name,
                        binary_stream.read(),
                        compress_type=zipfile.ZIP_DEFLATED
                    )
        except zipfile.BadZipfile:
            logger.exception("BadZipfile exception")
        content = stream.getvalue()
        headers = [
            ('Content-Type', 'zip'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Content-Length', len(content)),
            ('Content-Disposition',
             content_disposition((Name or 'undefined') + '.zip'))

        ]
        return request.make_response(content, headers)
