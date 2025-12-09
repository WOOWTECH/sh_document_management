# Bug Fix Plan: sh_document_management Module v0.0.3

## Overview
This plan addresses 2 bugs reported in BUG_REPORT.md for the sh_document_management Odoo 18 module.

## Project Context
- **Module:** sh_document_management (Document Management for Odoo 18)
- **Current Version:** 0.0.2
- **Target Version:** 0.0.3
- **Test Environment:** https://woowtech-testodoo.woowtech.io (admin/woowtech)

---

## Bug Summary

| Bug ID | Description | Severity | Status |
|--------|-------------|----------|--------|
| BUG-001 | Download action shows "Missing Action datas" error | High | Pending |
| BUG-002 | Share URL returns 404 Not Found | High | Pending |

---

## Task 1: Create Fix Plan (BACKEND-T001)

### BUG-001: Download Action Missing

**Symptom:** In "All Documents" kanban view, clicking "Download" from dropdown shows "Missing Action" popup saying action "datas" does not exist.

**Root Cause Analysis:**
The kanban dropdown menu in `views/ir_attachment_views.xml` (line 39) uses:
```xml
<a t-attf-href="/web/content/ir.attachment/#{record.id.raw_value}/datas?download=true" download="" class="dropdown-item">Download</a>
```

The issue is that Odoo 18's JavaScript framework intercepts anchor clicks inside kanban menus and tries to interpret them as action calls. The `download=""` attribute with no value and the specific href pattern causes the framework to look for an action named "datas" instead of following the URL.

**Fix Location:** `sh_document_management/views/ir_attachment_views.xml` (line 39)

**Solution:** Change the href format to use a simpler pattern that won't be intercepted.

**Recommended Fix:**
```xml
<a role="menuitem" class="dropdown-item" t-att-href="'/web/content/' + record.id.raw_value + '?download=true'">Download</a>
```

---

### BUG-002: Share URL 404 Not Found

**Symptom:** After sharing a document via email, clicking the "Download Attachment URL" in the email returns a 404 error.

**Root Cause Analysis:**
1. In `models/ir_attachment.py` (line 30), `_compute_full_url()` uses `self.access_token`
2. The base `ir.attachment` model has an `access_token` field, but it's NOT automatically generated
3. The `access_token` is only populated when `generate_access_token()` is called
4. The `action_share_directory()` method calls `_compute_full_url()` but never generates the token first
5. Result: The URL contains an empty/None token, which fails validation in the controller

**Fix Locations:**
1. `sh_document_management/models/ir_attachment.py` (lines 25-30)

**Solution:**
Before computing the share URL, ensure the access token is generated using Odoo's built-in `generate_access_token()` method.

**Recommended Fix:**
```python
def _compute_full_url(self):
    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    for record in self:
        # Generate access token if not exists (Odoo base method)
        if not record.access_token:
            record.generate_access_token()
        record.sh_share_url = base_url + '/attachment/download_directories' + \
            '?list_ids=%s&access_token=%s&name=%s' % (
                record.id, record.access_token, 'document')
```

---

## Task 2: Review Fix Plan (BACKEND-T002)

### Testing Cases

#### BUG-001 Test Cases:
1. Navigate to "All Documents" page
2. Hover on any document kanban card
3. Click dropdown menu (three dots)
4. Click "Download"
5. **Expected:** File downloads successfully
6. **Verify:** No "Missing Action" error popup

#### BUG-002 Test Cases:
1. Navigate to "All Documents" page
2. Click on any document to open form view
3. Assign a user to the document (sh_user_ids field)
4. Click Save
5. Click Share button
6. Check email received by assigned user
7. Click "Download Attachment URL" in email
8. **Expected:** File downloads successfully (as ZIP)
9. **Verify:** No 404 error page

### Acceptance Criteria
- [ ] BUG-001: Download from kanban dropdown works without error
- [ ] BUG-002: Share email link downloads the file successfully
- [ ] No regression in existing functionality
- [ ] Module loads without errors after update

---

## Task 3: Implement Fixes (BACKEND-T003)

### Implementation Steps

#### Step 1: Fix BUG-001 (Download Action)

**File:** `sh_document_management/views/ir_attachment_views.xml`

**Change:** Line 39

**From:**
```xml
<a t-attf-href="/web/content/ir.attachment/#{record.id.raw_value}/datas?download=true" download="" class="dropdown-item">Download</a>
```

**To:**
```xml
<a role="menuitem" class="dropdown-item" t-att-href="'/web/content/' + record.id.raw_value + '?download=true'">Download</a>
```

#### Step 2: Fix BUG-002 (Share URL Token)

**File:** `sh_document_management/models/ir_attachment.py`

**Change:** Lines 25-30

**From:**
```python
def _compute_full_url(self):
    base_url = self.env['ir.config_parameter'].sudo(
    ).get_param('web.base.url')
    self.sh_share_url = base_url + '/attachment/download_directories' + \
        '?list_ids=%s&access_token=%s&name=%s' % (
            self.id, self.access_token, 'document')
```

**To:**
```python
def _compute_full_url(self):
    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    for record in self:
        # Generate access token if not exists (Odoo base method)
        if not record.access_token:
            record.generate_access_token()
        record.sh_share_url = base_url + '/attachment/download_directories' + \
            '?list_ids=%s&access_token=%s&name=%s' % (
                record.id, record.access_token, 'document')
```

#### Step 3: Update Version

**File:** `sh_document_management/__manifest__.py`

**Change:** Line 12

**From:**
```python
"version": "0.0.2",
```

**To:**
```python
"version": "0.0.3",
```

#### Step 4: Update CHANGELOG.md

Add new section for version 0.0.3 with bug fixes.

---

## Critical Files to Modify

| File | Changes |
|------|---------|
| `sh_document_management/views/ir_attachment_views.xml` | Fix download href (line 39) |
| `sh_document_management/models/ir_attachment.py` | Add token generation (lines 25-30) |
| `sh_document_management/__manifest__.py` | Update version to 0.0.3 |
| `sh_document_management/CHANGELOG.md` | Add v0.0.3 section |

---

## Git Commit Strategy

1. **Commit 1:** `BUG-001: Fix download action in kanban dropdown`
2. **Commit 2:** `BUG-002: Generate access token before share URL computation`
3. **Commit 3:** `BACKEND-T005: Version update 0.0.3 and CHANGELOG`
