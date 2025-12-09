# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import random
import base64
import zipfile
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    directory_id = fields.Many2one('document.directory', string='Directory')
    document_tags = fields.Many2many('document.tags', string='Document Tags')
    color = fields.Integer(string='Color Index')
    sh_document_as_zip = fields.Boolean('Document as zip')
    sh_user_ids = fields.Many2many(
        'res.users', relation='rel_attachment_user', string='Users')

    sh_share_url = fields.Char(
        string="Link", compute='_compute_full_url')

    def _compute_full_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            # Generate access token if not exists (Odoo base method)
            if not record.access_token:
                record.generate_access_token()
            record.sh_share_url = base_url + '/attachment/download_directories' + \
                '?list_ids=%s&access_token=%s&name=%s' % (
                    record.id, record.access_token, 'document')

    def action_share_directory(self):
        self._compute_full_url()

        template = self.env.ref(
            "sh_document_management.sh_document_management_share_document_url_template")
        partner_to = ''
        total_receipients = len(self.sh_user_ids)
        count = 1
        if self.sh_user_ids:
            for resp in self.sh_user_ids:
                partner_to += str(resp.partner_id.id)
                if count < total_receipients:
                    partner_to += ','
                count += 1

        template.partner_to = partner_to
        # Get email sender with fallback (FIX-005)
        email_from = self.env.user.email or self.env.user.partner_id.email or \
            self.env['ir.mail_server'].sudo().search([], limit=1).smtp_user or \
            'noreply@example.com'
        template.sudo().send_mail(self.id, force_send=True, email_values={
            'email_from': email_from}, email_layout_xmlid='mail.mail_notification_light')

        # Return notification action (FIX-003)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Share Email Sent'),
                'message': _('Document share link has been sent to the selected users.'),
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def default_get(self, fields):
        rec = super(Attachment, self).default_get(fields)
        active_id = self._context.get("active_id")
        active_model = self._context.get("active_model")
        directory_id = None
        if active_id and active_model == 'document.directory':
            directory_id = active_id
        params = self._context.get("params")
        if not active_model and params and params.get("model") == 'document.directory':
            directory_id = params.get("id")
        if directory_id:
            rec.update({
                "directory_id": directory_id,
            })
        return rec

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            number = random.randrange(1, 10)
            values['color'] = number
        return super(Attachment, self).create(vals_list)

    def action_download_as_zip_attachment(self):
        """Export only selected attachments as ZIP (not entire directories)"""
        if self.env.context.get('active_ids'):
            attachment_ids = self.env['ir.attachment'].sudo().browse(
                self.env.context.get('active_ids'))

            if attachment_ids:
                mem_zip = BytesIO()
                with zipfile.ZipFile(mem_zip,
                                     mode="w",
                                     compression=zipfile.ZIP_DEFLATED) as zf:
                    for attachment in attachment_ids:
                        if attachment.datas:
                            # Sanitize filename - replace / with _ to avoid path issues
                            file_name = attachment.name.replace('/', '_') if attachment.name else 'attachment'
                            content = base64.b64decode(attachment.datas)
                            zf.writestr(file_name, content)

                content = base64.encodebytes(mem_zip.getvalue())
                if content:
                    get_attachment = self.env['ir.attachment'].sudo().create({
                        'name': 'Documents.zip',
                        'sh_document_as_zip': True,
                        'type': 'binary',
                        'mimetype': 'application/zip',
                        'datas': content
                    })
                    url = "/web/content/" + str(get_attachment.id) + "?download=true"
                    return {
                        'type': 'ir.actions.act_url',
                        'url': url,
                        'target': 'current',
                    }

    def action_document_preview(self):
        self.ensure_one()
        if self.type == 'url':
            if self.url:
                return {
                    'type': 'ir.actions.act_url',
                    'url': self.url,
                    'target': 'new',
                }
            else:
                raise UserError('Preview not available for this document.')
        else:
            if self.datas:
                if self.mimetype == 'text/plain' or self.mimetype == 'application/pdf' or self.mimetype == 'image/jpeg' or self.mimetype == 'image/jpg' or self.mimetype == 'image/png':
                    url = "/web/content/" + str(self.id)
                    return {
                        'type': 'ir.actions.act_url',
                        'url': url,
                        'target': 'new',
                    }
                else:
                    raise UserError(_('Preview not available for this document.'))
            else:
                raise UserError(_('Preview not available for this document.'))
