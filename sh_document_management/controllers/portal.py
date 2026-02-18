# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import base64
import io
import mimetypes
import zipfile
import logging

from odoo import http, _
from odoo.http import request, content_disposition, Response
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class DocumentPortal(CustomerPortal):
    """Portal controller for document management."""

    def _prepare_home_portal_values(self, counters):
        """Add document counts to portal home page."""
        values = super()._prepare_home_portal_values(counters)
        if 'document_count' in counters:
            partner = request.env.user.partner_id
            # Count directories shared with this portal user
            directory_count = request.env['document.directory'].sudo().search_count([
                ('portal_user_ids', 'in', [partner.id])
            ])
            # Count files directly shared with this portal user
            file_count = request.env['ir.attachment'].sudo().search_count([
                ('portal_user_ids', 'in', [partner.id])
            ])
            values['document_count'] = directory_count + file_count
        return values

    def _check_portal_access_directory(self, directory):
        """Check if current portal user can access the directory.

        Access is granted if:
        1. User's partner is directly in portal_user_ids
        2. Any parent directory has user's partner in portal_user_ids (inheritance)

        Args:
            directory: document.directory record

        Returns:
            bool: True if access is allowed

        Raises:
            AccessError: If access is denied
        """
        partner = request.env.user.partner_id

        # Check direct access
        if partner.id in directory.portal_user_ids.ids:
            return True

        # Check parent inheritance
        parent = directory.parent_id
        while parent:
            if partner.id in parent.portal_user_ids.ids:
                return True
            parent = parent.parent_id

        raise AccessError(_("You don't have access to this directory."))

    def _check_portal_access_attachment(self, attachment):
        """Check if current portal user can access the attachment.

        Access is granted if:
        1. User's partner is directly in attachment's portal_user_ids
        2. Attachment is in a directory user has access to (inheritance)

        Args:
            attachment: ir.attachment record

        Returns:
            bool: True if access is allowed

        Raises:
            AccessError: If access is denied
        """
        partner = request.env.user.partner_id

        # Check direct access to attachment
        if partner.id in attachment.portal_user_ids.ids:
            return True

        # Check directory access (inheritance)
        if attachment.directory_id:
            try:
                self._check_portal_access_directory(attachment.directory_id)
                return True
            except AccessError:
                pass

        raise AccessError(_("You don't have access to this file."))

    def _get_accessible_directories(self, partner):
        """Get all directories accessible to the portal user.

        Returns directories directly shared with the user.
        Sub-directories are accessible via inheritance but not listed separately.
        """
        return request.env['document.directory'].sudo().search([
            ('portal_user_ids', 'in', [partner.id])
        ])

    def _get_accessible_files(self, partner):
        """Get all files directly shared with the portal user.

        Does not include files in shared directories (those are accessed via directory).
        """
        return request.env['ir.attachment'].sudo().search([
            ('portal_user_ids', 'in', [partner.id]),
            ('directory_id', '=', False),  # Only files without directory
        ])

    def _get_files_directly_shared(self, partner):
        """Get files directly shared with portal user (including those in directories)."""
        return request.env['ir.attachment'].sudo().search([
            ('portal_user_ids', 'in', [partner.id])
        ])

    @http.route(['/my/documents', '/my/documents/page/<int:page>'],
                type='http', auth='user', website=True)
    def portal_my_documents(self, page=1, **kw):
        """Main portal page showing shared directories and files."""
        partner = request.env.user.partner_id

        # Get shared directories
        directories = self._get_accessible_directories(partner)

        # Get directly shared files (not in any directory OR explicitly shared)
        files = self._get_files_directly_shared(partner)

        values = {
            'directories': directories,
            'files': files,
            'page_name': 'documents',
            'default_url': '/my/documents',
        }
        return request.render('sh_document_management.portal_my_documents', values)

    @http.route(['/my/documents/directory/<int:directory_id>'],
                type='http', auth='user', website=True)
    def portal_directory_content(self, directory_id, **kw):
        """Show contents of a specific directory."""
        directory = request.env['document.directory'].sudo().browse(directory_id)

        if not directory.exists():
            return request.not_found()

        try:
            self._check_portal_access_directory(directory)
        except AccessError:
            return request.not_found()

        partner = request.env.user.partner_id

        # Get sub-directories (user can access these via inheritance)
        sub_directories = request.env['document.directory'].sudo().search([
            ('parent_id', '=', directory.id)
        ])

        # Get files in this directory
        files = request.env['ir.attachment'].sudo().search([
            ('directory_id', '=', directory.id)
        ])

        # Build breadcrumb
        breadcrumb = []
        current = directory
        while current:
            breadcrumb.insert(0, current)
            current = current.parent_id

        values = {
            'directory': directory,
            'sub_directories': sub_directories,
            'files': files,
            'breadcrumb': breadcrumb,
            'page_name': 'documents',
        }
        return request.render('sh_document_management.portal_directory_content', values)

    @http.route(['/my/documents/file/<int:file_id>/preview'],
                type='http', auth='user', website=True)
    def portal_file_preview(self, file_id, **kw):
        """Preview a file (PDF, images, text)."""
        attachment = request.env['ir.attachment'].sudo().browse(file_id)

        if not attachment.exists():
            return request.not_found()

        try:
            self._check_portal_access_attachment(attachment)
        except AccessError:
            return request.not_found()

        # Check if file is previewable
        previewable_mimetypes = [
            'application/pdf',
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp',
            'text/plain',
        ]

        if attachment.mimetype not in previewable_mimetypes:
            # Not previewable, redirect to download
            return request.redirect(f'/my/documents/file/{file_id}/download')

        if not attachment.datas:
            return request.not_found()

        # For PDF, render a viewer page with PDF.js
        if attachment.mimetype == 'application/pdf':
            values = {
                'file': attachment,
                'file_id': file_id,
            }
            return request.render('sh_document_management.portal_pdf_viewer', values)

        # For images and text, stream content directly
        content = base64.b64decode(attachment.datas)
        filename = (attachment.name or 'file').replace('"', '\\"')

        headers = [
            ('Content-Type', attachment.mimetype or 'application/octet-stream'),
            ('Content-Length', len(content)),
            ('X-Content-Type-Options', 'nosniff'),
            ('Cache-Control', 'no-cache'),
            ('Content-Disposition', f'inline; filename="{filename}"'),
        ]

        return request.make_response(content, headers)

    @http.route(['/my/documents/file/<int:file_id>/raw'],
                type='http', auth='user', website=True)
    def portal_file_raw(self, file_id, **kw):
        """Get raw file content for PDF.js viewer."""
        attachment = request.env['ir.attachment'].sudo().browse(file_id)

        if not attachment.exists():
            return request.not_found()

        try:
            self._check_portal_access_attachment(attachment)
        except AccessError:
            return request.not_found()

        if not attachment.datas:
            return request.not_found()

        content = base64.b64decode(attachment.datas)
        filename = (attachment.name or 'file').replace('"', '\\"')

        headers = [
            ('Content-Type', attachment.mimetype or 'application/octet-stream'),
            ('Content-Length', len(content)),
            ('X-Content-Type-Options', 'nosniff'),
            ('Cache-Control', 'no-cache'),
            ('Content-Disposition', f'inline; filename="{filename}"'),
            ('Accept-Ranges', 'bytes'),
        ]

        return request.make_response(content, headers)

    @http.route(['/my/documents/file/<int:file_id>/download'],
                type='http', auth='user', website=True)
    def portal_file_download(self, file_id, **kw):
        """Download a single file."""
        attachment = request.env['ir.attachment'].sudo().browse(file_id)

        if not attachment.exists():
            return request.not_found()

        try:
            self._check_portal_access_attachment(attachment)
        except AccessError:
            return request.not_found()

        # Stream file content directly (works through VPN/proxy)
        if not attachment.datas:
            return request.not_found()

        content = base64.b64decode(attachment.datas)
        headers = [
            ('Content-Type', attachment.mimetype or 'application/octet-stream'),
            ('Content-Length', len(content)),
            ('Content-Disposition', content_disposition(attachment.name or 'download')),
            ('X-Content-Type-Options', 'nosniff'),
        ]
        return request.make_response(content, headers)

    @http.route(['/my/documents/directory/<int:directory_id>/download'],
                type='http', auth='user', website=True)
    def portal_directory_download(self, directory_id, **kw):
        """Download all files in a directory as ZIP."""
        directory = request.env['document.directory'].sudo().browse(directory_id)

        if not directory.exists():
            return request.not_found()

        try:
            self._check_portal_access_directory(directory)
        except AccessError:
            return request.not_found()

        # Get all files in this directory (and subdirectories)
        def get_all_files(dir_record, path=''):
            """Recursively get all files with their paths."""
            files = []
            current_path = f"{path}/{dir_record.name}" if path else dir_record.name

            # Files in current directory
            for attachment in dir_record.attachment_ids:
                if attachment.datas:
                    file_name = (attachment.name or 'file').replace('/', '_')
                    files.append({
                        'path': f"{current_path}/{file_name}",
                        'data': attachment.datas,
                    })

            # Recursively get files from subdirectories
            for subdir in request.env['document.directory'].sudo().search([
                ('parent_id', '=', dir_record.id)
            ]):
                files.extend(get_all_files(subdir, current_path))

            return files

        all_files = get_all_files(directory)

        if not all_files:
            # Empty directory
            return request.not_found()

        # Create ZIP in memory
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for file_info in all_files:
                content = base64.b64decode(file_info['data'])
                zf.writestr(file_info['path'], content)

        content = mem_zip.getvalue()
        headers = [
            ('Content-Type', 'application/zip'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Content-Length', len(content)),
            ('Content-Disposition', content_disposition(f"{directory.name}.zip")),
        ]
        return request.make_response(content, headers)
