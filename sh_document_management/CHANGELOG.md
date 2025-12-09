# Changelog

All notable changes to the `sh_document_management` module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.5] - 2025-12-09

### Fixed

#### BUG-002: Share URL Shows Local Address (Auto-Detection Fix)
- **Issue**: Share email download links showed local IP (192.168.2.6) instead of public URL when admin logged in via local IP
- **Root Cause**: `web.base.url` auto-updates on every admin login; local login overwrites public URL with local IP
- **Solution**: Implemented intelligent auto-detection system that:
  1. Monitors `web.base.url` changes via `ir.config_parameter` model inheritance
  2. Automatically detects if URL is public (domain/public IP) vs private (192.168.x.x, 10.x.x.x, etc.)
  3. Saves public URLs to `sh_document_management.public_base_url` parameter
  4. Share URLs always use the saved public URL (with fallback to `web.base.url`)
- **User Experience**: Zero manual configuration required - system learns public URL automatically
- **Private IP Detection**: Rejects 10.x.x.x, 172.16-31.x.x, 192.168.x.x, localhost, .local domains
- **Affected Files**:
  - `models/ir_config_parameter.py` (new file - auto-detection logic)
  - `models/__init__.py` (import new model)
  - `__init__.py` (post_init_hook for initialization)
  - `models/ir_attachment.py` (use public_base_url)
  - `models/document_directory.py` (use public_base_url)
  - `__manifest__.py` (version, post_init_hook)

---

## [0.0.4] - 2025-12-09

### Fixed

#### BUG-001: Download Action in Kanban View (Final Fix)
- **Issue**: Clicking "Download" in document kanban dropdown still showed "Missing Action content" error
- **Root Cause**: Odoo 18's kanban menu system intercepts ALL anchor tag clicks inside `<t t-name="kanban-menu">` and tries to interpret them as Odoo actions, parsing "content" from `/web/content/...` as an action name
- **Solution**: Changed from `<a href>` to `<button type="object" name="action_download">` which properly returns an `ir.actions.act_url` action
- **Affected Files**:
  - `models/ir_attachment.py` (new `action_download()` method)
  - `views/ir_attachment_views.xml` (line 39: changed anchor to button)

#### BUG-002: Share URL Shows Local Address (Configuration Fix)
- **Issue**: Share email download link showed local IP (192.168.2.6) instead of public URL
- **Root Cause**: Cloudflare Tunnel doesn't pass `X-Forwarded-Host` header to Odoo, preventing auto-detection of public URL
- **Solution**: Configure Cloudflare Tunnel HTTP Host Header setting (no code change required)
- **User Action Required**:
  1. Go to Cloudflare Zero Trust Dashboard → Networks → Tunnels
  2. Edit hostname configuration for your Odoo domain
  3. Under HTTP Settings, set "HTTP Host Header" to your public domain
  4. Save and re-login to Odoo as admin to trigger `web.base.url` auto-update

---

## [0.0.3] - 2025-12-09

### Fixed

#### BUG-001: Download Action in Kanban View
- **Issue**: Clicking "Download" in document kanban dropdown showed "Missing Action datas" error
- **Cause**: Anchor tag href pattern `/web/content/ir.attachment/{id}/datas?download=true` was intercepted by Odoo 18 JS framework as an action call instead of a direct URL
- **Solution**: Changed href format to use simpler `/web/content/{id}?download=true` pattern
- **Affected Files**:
  - `views/ir_attachment_views.xml` (line 39)

#### BUG-002: Share URL Returns 404
- **Issue**: Share email download link returned 404 Not Found when clicked
- **Cause**: Access token was not generated before creating share URL; `access_token` field was empty/None
- **Solution**: Added `generate_access_token()` call before computing share URL to ensure token exists
- **Affected Files**:
  - `models/ir_attachment.py` (lines 25-33)

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

### Upgrading from 0.0.4 to 0.0.5

1. **Backup**: Create a database backup before upgrading
2. **Update Module**: Click "Update" in Apps menu or run `-u sh_document_management`
3. **First Public Login Required**: After upgrade, login via public URL once to trigger auto-detection
4. **Verification** (optional):
   - Go to Settings → Technical → Parameters → System Parameters
   - Search for `sh_document_management.public_base_url`
   - Should contain your public URL (e.g., `https://woowtech-testodoo.woowtech.io`)
5. **Test**: Share a document and verify email contains public URL

### Upgrading from 0.0.3 to 0.0.4

1. **Backup**: Create a database backup before upgrading
2. **Update Module**: Click "Update" in Apps menu or run `-u sh_document_management`
3. **No Data Migration Required**: All fixes are code-level improvements
4. **Cloudflare Configuration** (for BUG-002):
   - Go to Cloudflare Zero Trust Dashboard → Networks → Tunnels
   - Edit hostname for your Odoo domain
   - Under HTTP Settings, set "HTTP Host Header" to your public domain (e.g., `woowtech-testodoo.woowtech.io`)
   - Save and re-login to Odoo as admin

### Upgrading from 0.0.2 to 0.0.3

1. **Backup**: Create a database backup before upgrading
2. **Update Module**: Click "Update" in Apps menu or run `-u sh_document_management`
3. **No Data Migration Required**: All fixes are code-level improvements
4. **Share Links**: Existing share links may need to be regenerated (access tokens will be created on first share)

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
