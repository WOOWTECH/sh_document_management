# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import random
import base64
import zipfile
import io
import uuid
from odoo import models, fields, api, _


class Directory(models.Model):
    _name = 'document.directory'
    _description = 'Document Directory'
    _rec_name = 'name'

    sequence = fields.Integer()
    name = fields.Char(required=True)
    image_medium = fields.Binary(string='Image')
    image_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    file_count = fields.Integer(compute='_compute_counts', string="File Count")
    sub_directory_count = fields.Integer(compute='_compute_counts', string="Sub Directory Count")
    parent_id = fields.Many2one('document.directory', 'Parent Directory')
    visible_directory = fields.Boolean(string='Visible Directory')
    directory_tag_ids = fields.Many2many(
        'directory.tags', string='Directory Tags')
    attachment_ids = fields.One2many(
        'ir.attachment', 'directory_id', string=" Files")
    directory_ids = fields.Many2many(
        'document.directory', compute='_compute_counts')
    # HIGH-002 FIX: Consolidated duplicate fields - use file_count and sub_directory_count directly
    files = fields.Integer(string="Files", related='file_count')
    sub_directories = fields.Integer(string="Sub Directories", related='sub_directory_count')
    color = fields.Integer(string='Color Index')
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    sh_user_ids = fields.Many2many(
        'res.users', relation='rel_directory_user', string='Users')

    sh_share_url = fields.Char(
        string="Link", compute='_compute_full_url')

    sh_access_token = fields.Char("Access Token")

    @api.model
    def default_get(self, fields):
        rec = super(Directory, self).default_get(fields)
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
                "parent_id": directory_id,
            })
        return rec


    def _get_token(self):
        """ Get the current record access token """
        if self.sh_access_token:
            return self.sh_access_token
        else:
            sh_access_token = str(uuid.uuid4())
            self.write({'sh_access_token': sh_access_token})
            return sh_access_token

    def _compute_full_url(self):
        """Compute the public share URL for each directory.

        MEDIUM-003 FIX: Handle multiple records properly by iterating over self.
        """
        IrConfig = self.env['ir.config_parameter'].sudo()
        # Use auto-detected public URL, fall back to web.base.url (BUG-002 fix)
        base_url = IrConfig.get_param('sh_document_management.public_base_url') or \
                   IrConfig.get_param('web.base.url')
        for record in self:
            record.sh_share_url = f"{base_url}/attachment/download_directories?list_ids={record.id}&access_token={record._get_token()}&name=directory"

    def action_share_directory(self):
        self._compute_full_url()

        template = self.env.ref(
            "sh_document_management.sh_document_management_share_directory_url_template")
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
                'message': _('Directory share link has been sent to the selected users.'),
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def _run_auto_delete_garbage_collection(self):
        attachment_ids = self.env['ir.attachment'].sudo().search(
            [('sh_document_as_zip', '=', True)])
        if attachment_ids:
            attachment_ids.sudo().unlink()

    def action_download_as_zip(self):
        """Export selected directories as a ZIP file.

        HIGH-003 FIX: Use writestr() instead of writing to disk.
        HIGH-005 FIX: Removed unsafe file handle usage.
        """
        if not self.env.context.get('active_ids'):
            return

        directory_ids = self.env['document.directory'].sudo().browse(
            self.env.context.get('active_ids'))
        if not directory_ids:
            return

        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for directory in directory_ids:
                dir_name = directory.name or 'directory'
                documents = self.env['ir.attachment'].sudo().search(
                    [('directory_id', '=', directory.id)])
                for attachment in documents:
                    if not attachment.datas:
                        continue
                    # Sanitize filename to prevent path traversal
                    attachment_name = (attachment.name or 'attachment').replace('/', '_')
                    # Create path within ZIP: directory_name/filename
                    zip_path = f"{dir_name}/{attachment_name}"
                    # HIGH-003 FIX: Write directly to ZIP from memory
                    content = base64.b64decode(attachment.datas)
                    zf.writestr(zip_path, content)

        content = base64.encodebytes(mem_zip.getvalue())
        if content:
            get_attachment = self.env['ir.attachment'].sudo().create({
                'name': 'Documents.zip',
                'sh_document_as_zip': True,
                'type': 'binary',
                'mimetype': 'application/zip',
                'datas': content
            })
            url = f"/web/content/{get_attachment.id}?download=true"
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'current',
            }

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            sequence = self.env['ir.sequence'].next_by_code(
                'document.directory')
            number = random.randrange(1, 10)
            values['sequence'] = sequence
            values['color'] = number
        return super(Directory, self).create(vals_list)

    def _compute_counts(self):
        """Compute file count, sub-directory count, and directory_ids.

        HIGH-001 FIX: Use read_group for batch counting instead of N+1 queries.
        HIGH-002 FIX: Consolidated all count computations into single method.
        """
        if not self:
            return

        # Batch count files using read_group
        attachment_data = self.env['ir.attachment'].sudo().read_group(
            [('directory_id', 'in', self.ids)],
            ['directory_id'],
            ['directory_id']
        )
        file_count_map = {
            d['directory_id'][0]: d['directory_id_count']
            for d in attachment_data if d['directory_id']
        }

        # Batch count sub-directories using read_group
        subdir_data = self.env['document.directory'].sudo().read_group(
            [('parent_id', 'in', self.ids)],
            ['parent_id'],
            ['parent_id']
        )
        subdir_count_map = {
            d['parent_id'][0]: d['parent_id_count']
            for d in subdir_data if d['parent_id']
        }

        # Get actual sub-directory records for directory_ids field
        all_subdirs = self.env['document.directory'].sudo().search(
            [('parent_id', 'in', self.ids)]
        )
        subdir_ids_map = {}
        for subdir in all_subdirs:
            parent_id = subdir.parent_id.id
            if parent_id not in subdir_ids_map:
                subdir_ids_map[parent_id] = []
            subdir_ids_map[parent_id].append(subdir.id)

        # Assign values to each record
        for rec in self:
            rec.file_count = file_count_map.get(rec.id, 0)
            rec.sub_directory_count = subdir_count_map.get(rec.id, 0)
            rec.directory_ids = [(6, 0, subdir_ids_map.get(rec.id, []))]

    def action_view_sub_directory(self):
        if self:
            for rec in self:
                return {
                    'name': _('Sub Directories'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'document.directory',
                    'view_type': 'form',
                    'view_mode': 'kanban,list,form',
                    'domain': [('parent_id', '=', rec.id)],
                    'target': 'current'
                }

    def action_view_files(self):
        if self:
            for rec in self:
                return {
                    'name': _('Files'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'ir.attachment',
                    'view_type': 'form',
                    'view_mode': 'kanban,list,form',
                    'domain': [('directory_id', '=', rec.id)],
                    'target': 'current'
                }

    def action_view(self):
        if self:
            return {
                'name': _('Files'),
                'type': 'ir.actions.act_window',
                        'res_model': 'ir.attachment',
                        'view_type': 'form',
                        'view_mode': 'kanban,list,form',
                        'domain': [('directory_id', '=', self.id)],
                        'target': 'current'
            }
