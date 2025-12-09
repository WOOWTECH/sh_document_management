# Changelog

All notable changes to the `sh_document_management` module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.2] - 2025-12-09

### Fixed

#### FIX-001: Cross-Platform Temp Directory
- **Issue**: Hardcoded `/tmp` path caused failures on Windows systems
- **Solution**: Replaced with `tempfile.gettempdir()` for cross-platform compatibility
- **Affected Files**:
  - `models/document_directory.py` (line 123)
  - `models/ir_attachment.py` (line 93)

#### FIX-002: Token Validation in Public Controller
- **Issue**: Public download route lacked explicit access token validation
- **Solution**: Added parameter validation and token verification; returns 404 for invalid requests
- **Security**: Prevents unauthorized access to shared directories/documents
- **Affected Files**:
  - `controllers/sh_download_directories.py`

#### FIX-003: Share Button Feedback
- **Issue**: Share button had no user feedback after sending email
- **Solution**: Added `ir.actions.client` display notification showing success message
- **User Experience**: Users now see "Share Email Sent" notification after sharing
- **Affected Files**:
  - `models/document_directory.py`
  - `models/ir_attachment.py`

#### FIX-004: URL Route Typo with Backward Compatibility
- **Issue**: Route URL had typo (`download_directiries` instead of `download_directories`)
- **Solution**: Added correct URL route while maintaining backward compatibility with old URL
- **Backward Compatible**: Both old and new URLs work to avoid breaking existing shared links
- **Affected Files**:
  - `controllers/sh_download_directories.py`

#### FIX-005: Email Sender Fallback
- **Issue**: `action_share_directory()` failed when user had no email configured
- **Solution**: Added fallback chain: user email -> partner email -> mail server -> default
- **Affected Files**:
  - `models/document_directory.py`
  - `models/ir_attachment.py`

#### FIX-006: ZIP Export Selected Files Only
- **Issue**: `action_download_as_zip_attachment()` exported entire directories instead of selected files
- **Solution**: Rewrote method to export only the specifically selected attachments
- **Affected Files**:
  - `models/ir_attachment.py`

#### FIX-007: "Directory Tags" Label Typo
- **Issue**: Field label displayed "Diractory Tags" instead of "Directory Tags"
- **Solution**: Corrected spelling in field string
- **Affected Files**:
  - `models/document_directory.py`

#### FIX-008: Method Name Typo
- **Issue**: Method named `_run_auto_delete_garbase_collection` (misspelled "garbage")
- **Solution**: Renamed to `_run_auto_delete_garbage_collection`
- **Affected Files**:
  - `models/document_directory.py`
  - `data/ir_cron_data.xml`

#### FIX-009: Cron Data Filename Typo
- **Issue**: File named `ir_crom_data.xml` (misspelled "cron")
- **Solution**: Renamed to `ir_cron_data.xml`
- **Affected Files**:
  - `data/ir_cron_data.xml` (renamed from `ir_crom_data.xml`)
  - `__manifest__.py` (updated reference)

#### FIX-010: Remove Incomplete Wizard Model
- **Issue**: `sh.share.directories` wizard had undefined `_compute_full_url` method causing errors
- **Solution**: Removed incomplete wizard model; functionality handled by directory/attachment models
- **Affected Files**:
  - `wizard/__init__.py` (import removed)
  - `wizard/sh_share_directories.py` (deleted)
  - `security/ir.model.access.csv` (access rule removed)

---

## [0.0.1] - Initial Release

### Added
- Document directory management with hierarchical structure
- File upload and organization within directories
- Directory and document tagging system
- Sharing functionality with access tokens
- ZIP export for directories and documents
- Document preview (PDF, images, text files)
- Multi-company support
- User group permissions (User, Manager)
- Custom kanban views for documents
- Search and filter capabilities
- Scheduled cleanup of temporary ZIP files

---

## Upgrade Notes

### Upgrading from 0.0.1 to 0.0.2

1. **Backup**: Create a database backup before upgrading
2. **Update Module**: Click "Update" in Apps menu or run `-u sh_document_management`
3. **Shared Links**: Existing shared links will continue to work (backward compatible)
4. **No Data Migration Required**: All fixes are code-level improvements

### Known Compatibility

- **Odoo Version**: 18.0
- **Python Version**: 3.10+
- **Operating Systems**: Linux, Windows, macOS (cross-platform temp directory fix)

---

## Contributors

- Softhealer Technologies (original development)
- Claude Code AI Assistant (bug fixes and improvements)

---

## Support

For issues or feature requests:
- **Email**: support@softhealer.com
- **Website**: https://www.softhealer.com
