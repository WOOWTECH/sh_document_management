# FIX_PLAN.md - sh_document_management Module

## Overview

This document outlines the comprehensive fix plan for all issues identified during testing (TST-T001) and code review (ARC-T001).

**Total Issues:** 10
**Priority 1 (Must Fix):** 3
**Priority 2 (Should Fix):** 4
**Priority 3 (Nice to Have):** 3

---

## Priority 1 - Must Fix

### FIX-001: Cross-Platform Temp Directory

**Issue:** CODE-002 - Hardcoded `/tmp` path causes Windows incompatibility

**Severity:** High

**Affected Files:**
- `models/document_directory.py` (line 123)
- `models/ir_attachment.py` (line 93)

**Current Code:**
```python
path_main = os.path.join('/tmp')
```

**Fixed Code:**
```python
import tempfile
path_main = tempfile.gettempdir()
```

**Testing:**
- [ ] Verify ZIP export works on Linux
- [ ] Verify ZIP export works on Windows
- [ ] Verify temp files are cleaned up

---

### FIX-002: Token Validation in Public Controller

**Issue:** CODE-007 - Missing explicit token validation in public download controller

**Severity:** Medium (Security)

**Affected Files:**
- `controllers/sh_download_directories.py` (lines 14-63)

**Current Code:**
```python
def sh_download_directiries(self, list_ids='', access_token='', name='', **post):
    if not list_ids:
        return request.not_found()
    # No token validation...
```

**Fixed Code:**
```python
def sh_download_directiries(self, list_ids='', access_token='', name='', **post):
    if not list_ids or not access_token:
        return request.not_found()

    # Validate token based on type
    if name == 'directory':
        record = request.env['document.directory'].sudo().browse(int(list_ids))
        if not record.exists() or record.sh_access_token != access_token:
            return request.not_found()
    elif name == 'document':
        record = request.env['ir.attachment'].sudo().browse(int(list_ids))
        if not record.exists() or record.sh_access_token != access_token:
            return request.not_found()
    else:
        return request.not_found()
    # Continue with download...
```

**Testing:**
- [ ] Verify valid token allows download
- [ ] Verify invalid token returns 404
- [ ] Verify missing token returns 404

---

### FIX-003: Share Action Feedback

**Issue:** BUG-002 - No user feedback after Share action

**Severity:** Medium (UX)

**Affected Files:**
- `models/document_directory.py` (lines 89-106)
- `models/ir_attachment.py` (similar method)

**Current Code:**
```python
def action_share_directory(self):
    self._compute_full_url()
    # ... send email ...
    # Returns None (no feedback)
```

**Fixed Code:**
```python
def action_share_directory(self):
    self._compute_full_url()
    # ... send email ...
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Share Email Sent',
            'message': 'Directory share link has been sent to the selected users.',
            'type': 'success',
            'sticky': False,
        }
    }
```

**Testing:**
- [ ] Verify notification appears after clicking Share
- [ ] Verify notification message is correct
- [ ] Verify notification auto-dismisses

---

## Priority 2 - Should Fix

### FIX-004: URL Route Typo (with Backward Compatibility)

**Issue:** CODE-001 - URL route typo `/attachment/download_directiries`

**Severity:** Medium

**Affected Files:**
- `controllers/sh_download_directories.py` (line 14)
- `models/document_directory.py` (line 85)
- `models/ir_attachment.py` (similar line)

**Fix Strategy:**
1. Add new correct route
2. Keep old route for backward compatibility with existing shared links
3. Both routes call same method

**Fixed Code (Controller):**
```python
@http.route(['/attachment/download_directories', '/attachment/download_directiries'],
            type='http', auth='public', website=False, csrf=False)
def sh_download_directories(self, list_ids='', access_token='', name='', **post):
    # ... existing logic ...
```

**Fixed Code (Models):**
```python
# In _compute_full_url()
self.sh_share_url = base_url + '/attachment/download_directories' + \
    '?list_ids=%s&access_token=%s&name=%s' % (
        self.id, self._get_token(), 'directory')
```

**Testing:**
- [ ] Verify new URL works
- [ ] Verify old URL still works (backward compatibility)
- [ ] Verify newly generated share URLs use correct spelling

---

### FIX-005: Email Sender Fallback

**Issue:** CODE-005 - `self.env.user.email` may be empty

**Severity:** Medium

**Affected Files:**
- `models/document_directory.py` (line 106)
- `models/ir_attachment.py` (similar line)

**Current Code:**
```python
template.sudo().send_mail(self.id, force_send=True, email_values={
    'email_from': self.env.user.email}, ...)
```

**Fixed Code:**
```python
email_from = self.env.user.email or self.env.user.partner_id.email or \
    self.env['ir.mail_server'].sudo().search([], limit=1).smtp_user or \
    'noreply@example.com'
template.sudo().send_mail(self.id, force_send=True, email_values={
    'email_from': email_from}, ...)
```

**Testing:**
- [ ] Verify email sends when user has email
- [ ] Verify email sends when user has no email (fallback works)
- [ ] Verify email has valid From address

---

### FIX-006: ZIP Export Selected Files Only

**Issue:** CODE-006 - ZIP export exports entire directories instead of selected files

**Severity:** Medium

**Affected Files:**
- `models/ir_attachment.py` (lines 78-137)

**Current Behavior:** Selecting 3 files exports ALL files from those files' directories

**Expected Behavior:** Export only the selected files

**Fixed Code:**
```python
def action_download_as_zip_attachment(self):
    if self.env.context.get('active_ids'):
        attachment_ids = self.env['ir.attachment'].sudo().browse(
            self.env.context.get('active_ids'))

        if attachment_ids:
            mem_zip = BytesIO()
            with zipfile.ZipFile(mem_zip, mode="w",
                                 compression=zipfile.ZIP_DEFLATED) as zf:
                for attachment in attachment_ids:
                    if attachment.datas:
                        file_name = attachment.name.replace('/', '_') if attachment.name else 'attachment'
                        content = base64.b64decode(attachment.datas)
                        zf.writestr(file_name, content)

            content = base64.encodebytes(mem_zip.getvalue())
            # Create temporary attachment and return download URL...
```

**Testing:**
- [ ] Select 3 files from different directories
- [ ] Export as ZIP
- [ ] Verify ZIP contains only 3 selected files (not entire directories)

---

### FIX-007: Form Label Typo

**Issue:** BUG-001 - "Diractory Tags" typo in form label

**Severity:** Minor (UI)

**Affected Files:**
- `views/document_directory_views.xml`

**Current Code:**
```xml
<field name="directory_tag_ids" widget="many2many_tags" ... string="Diractory Tags"/>
```

**Fixed Code:**
```xml
<field name="directory_tag_ids" widget="many2many_tags" ... string="Directory Tags"/>
```

**Also check model field definition:**
- `models/document_directory.py` (line 34)

**Testing:**
- [ ] Verify form shows "Directory Tags" label
- [ ] Verify no other typos in UI labels

---

## Priority 3 - Nice to Have

### FIX-008: Method Name Typo

**Issue:** CODE-003 - Method name `_run_auto_delete_garbase_collection`

**Severity:** Minor (Code Quality)

**Affected Files:**
- `models/document_directory.py` (line 109)
- `data/ir_crom_data.xml` (cron definition)

**Fix:**
1. Rename method to `_run_auto_delete_garbage_collection`
2. Update cron XML to call new method name

**Testing:**
- [ ] Verify cron job still runs correctly
- [ ] Verify ZIP files are cleaned up

---

### FIX-009: Cron File Name Typo

**Issue:** CODE-004 - File name `ir_crom_data.xml` should be `ir_cron_data.xml`

**Severity:** Minor (Code Quality)

**Affected Files:**
- `data/ir_crom_data.xml` (rename to `ir_cron_data.xml`)
- `__manifest__.py` (update data file reference)

**Testing:**
- [ ] Verify module still installs correctly
- [ ] Verify cron job is registered

---

### FIX-010: Remove Incomplete Wizard

**Issue:** CODE-008 - Incomplete wizard model `sh_share_directories`

**Severity:** Low (Dead Code)

**Affected Files:**
- `wizard/sh_share_directories.py`
- `wizard/__init__.py`
- `security/ir.model.access.csv`

**Options:**
A. Remove the incomplete wizard entirely
B. Complete the implementation

**Recommended:** Option A - Remove dead code

**Testing:**
- [ ] Verify module still installs correctly
- [ ] Verify no references to removed model

---

## Implementation Order

1. **FIX-001** - Cross-platform temp directory (High priority, low risk)
2. **FIX-002** - Token validation (Security fix)
3. **FIX-003** - Share feedback notification (UX improvement)
4. **FIX-007** - Form label typo (Quick fix)
5. **FIX-004** - URL route typo (with backward compatibility)
6. **FIX-005** - Email sender fallback
7. **FIX-006** - ZIP export selected files only
8. **FIX-008** - Method name typo
9. **FIX-009** - Cron file name typo
10. **FIX-010** - Remove incomplete wizard

---

## Testing Checklist

### Pre-Implementation
- [ ] Create new git branch: `fix/module-fixes`
- [ ] Backup current module state

### Post-Implementation
- [ ] All unit tests pass
- [ ] Manual testing on Linux
- [ ] Manual testing on Windows (if available)
- [ ] Re-run all functional tests from TST-T001
- [ ] Verify backward compatibility

### Regression Testing
- [ ] Directory creation still works
- [ ] File upload still works
- [ ] ZIP export still works
- [ ] Sharing still works
- [ ] Search/filter still works
- [ ] Cron job still runs

---

## Estimated Impact

| Fix | Files Changed | Lines Changed | Risk Level |
|-----|---------------|---------------|------------|
| FIX-001 | 2 | ~4 | Low |
| FIX-002 | 1 | ~15 | Medium |
| FIX-003 | 2 | ~20 | Low |
| FIX-004 | 3 | ~6 | Low |
| FIX-005 | 2 | ~8 | Low |
| FIX-006 | 1 | ~30 | Medium |
| FIX-007 | 1 | ~2 | Low |
| FIX-008 | 2 | ~4 | Low |
| FIX-009 | 2 | ~2 | Low |
| FIX-010 | 3 | ~50 (removal) | Low |

**Total:** ~141 lines changed across 10 files

---

## Success Criteria

All fixes are considered complete when:

1. All 10 issues are resolved
2. All tests from INVESTIGATION_TEST_RESULT.md pass
3. No new bugs introduced (regression testing)
4. Module installs cleanly on fresh Odoo 18 instance
5. Cross-platform compatibility verified
6. Code review approved

---

## REV-T001: Fix Plan Review Notes

**Review Date:** 2025-12-08
**Reviewer:** Claude Code Agent

### Verification Summary

| Fix ID | File Verification | Code Location Confirmed | Fix Approach Valid |
|--------|-------------------|------------------------|-------------------|
| FIX-001 | VERIFIED | `document_directory.py:123`, `ir_attachment.py:93` | YES |
| FIX-002 | VERIFIED | `sh_download_directories.py:14-63` | YES (Enhanced) |
| FIX-003 | VERIFIED | `document_directory.py:89-106`, `ir_attachment.py:35-52` | YES |
| FIX-004 | VERIFIED | Controller route, model URLs | YES |
| FIX-005 | VERIFIED | `document_directory.py:106`, `ir_attachment.py:52` | YES |
| FIX-006 | VERIFIED | `ir_attachment.py:78-137` | YES |
| FIX-007 | VERIFIED | `document_directory.py:34` | YES |
| FIX-008 | VERIFIED | `document_directory.py:109`, `ir_crom_data.xml:8` | YES |
| FIX-009 | VERIFIED | `__manifest__.py:24` | YES |
| FIX-010 | VERIFIED | `wizard/sh_share_directories.py`, `ir.model.access.csv:5` | YES |

### Enhanced Notes for FIX-002

**Critical Finding:** The controller signature on line 15 is:
```python
def sh_download_directiries(self, list_ids='', name='', **post):
```

The `access_token` parameter is NOT explicitly defined - it would only be captured in `**post`. This needs to be fixed to:
```python
def sh_download_directories(self, list_ids='', access_token='', name='', **post):
```

### Files to Modify (Final List)

| File | Fixes |
|------|-------|
| `models/document_directory.py` | FIX-001, FIX-003, FIX-005, FIX-007, FIX-008 |
| `models/ir_attachment.py` | FIX-001, FIX-003, FIX-005, FIX-006 |
| `controllers/sh_download_directories.py` | FIX-002, FIX-004 |
| `data/ir_crom_data.xml` | FIX-008, FIX-009 (rename file) |
| `__manifest__.py` | FIX-009 (update reference) |
| `wizard/sh_share_directories.py` | FIX-010 (delete file) |
| `wizard/__init__.py` | FIX-010 (remove import) |
| `security/ir.model.access.csv` | FIX-010 (remove line 5) |

### Review Status: APPROVED

All fixes have been verified against source code. Implementation can proceed.

---

**Document Version**: 1.1
**Last Updated**: 2025-12-08
**Task ID**: FIX-T001 (Created), REV-T001 (Reviewed)
