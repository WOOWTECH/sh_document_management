# CLAUDE.md - sh_document_management Module

## Table of Contents
1. [Module Overview](#module-overview)
2. [Directory Structure](#directory-structure)
3. [Data Models](#data-models)
4. [Views & UI](#views--ui)
5. [Controllers & Routes](#controllers--routes)
6. [Security](#security)
7. [Key Features](#key-features)
8. [JavaScript Components](#javascript-components)
9. [Development Guidelines](#development-guidelines)
10. [Known Issues & TODOs](#known-issues--todos)

---

## Module Overview

### Basic Information
- **Name**: Document Management
- **Technical Name**: sh_document_management
- **Version**: 0.0.1
- **Author**: Softhealer Technologies
- **License**: OPL-1
- **Category**: Document Management
- **Website**: https://www.softhealer.com
- **Price**: 24.83 EUR

### Purpose
This module provides a comprehensive document management system for Odoo 18, allowing users to:
- Organize files in hierarchical directory structures
- Tag and categorize documents and directories
- Share documents and directories via email with access tokens
- Export documents as ZIP files
- Preview documents directly in the browser
- Control access through user permissions and visibility settings

### Dependencies
- `base` - Core Odoo framework
- `mail` - Email functionality for sharing features
- `web` - Web interface components

### Application Status
- **Application**: True (appears as a main app in the Apps menu)
- **Auto-install**: False (must be manually installed)
- **Installable**: True

---

## Directory Structure

```
sh_document_management/
├── __init__.py                          # Root module initializer
├── __manifest__.py                      # Module manifest/configuration
├── README.md                            # Installation and usage guide
│
├── controllers/                         # HTTP Controllers
│   ├── __init__.py
│   └── sh_download_directories.py       # ZIP download controller
│
├── data/                                # Data files
│   ├── ir_crom_data.xml                 # Scheduled action (cron job)
│   └── mail_template_data.xml           # Email templates for sharing
│
├── doc/                                 # Documentation
│   └── changelog.rst                    # Version history
│
├── i18n/                                # Translations
│   ├── sh_document_management.pot       # Translation template
│   └── zh_HK.po                         # Hong Kong Chinese translation
│
├── models/                              # Data models
│   ├── __init__.py
│   ├── directory_tags.py                # Directory tag model
│   ├── document_tags.py                 # Document tag model
│   ├── document_directory.py            # Main directory model
│   └── ir_attachment.py                 # Extended attachment model
│
├── security/                            # Access control
│   ├── ir.model.access.csv              # Model access rights
│   └── sh_document_management_groups.xml # Groups and record rules
│
├── static/                              # Frontend assets
│   ├── description/                     # Module description & images
│   │   ├── icon.png                     # Module icon
│   │   ├── menu_icon.png                # Menu icon
│   │   ├── index.html                   # Module description page
│   │   └── screenshots/                 # Feature screenshots
│   └── src/                             # JavaScript/CSS source
│       └── views/
│           └── sh_documents_kanban/     # Custom kanban view
│               ├── document_management_kanban_view.js
│               ├── document_management_kanban_renderer.js
│               └── document_management_kanban_record.js
│
├── views/                               # XML view definitions
│   ├── directory_tags_views.xml         # Directory tags views
│   ├── document_tags_views.xml          # Document tags views
│   ├── document_directory_views.xml     # Directory views & actions
│   ├── ir_attachment_views.xml          # Attachment views
│   └── menus.xml                        # Menu structure
│
└── wizard/                              # Transient models
    ├── __init__.py
    └── sh_share_directories.py          # Share wizard (incomplete)
```

---

## Data Models

### 1. document.directory

**File**: `models/document_directory.py`

Main model representing a directory/folder in the document management system.

#### Key Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `sequence` | Integer | Ordering sequence for directories |
| `name` | Char | Directory name (required) |
| `image_medium` | Binary | Medium-sized directory icon |
| `image_small` | Binary | Small-sized directory icon (64x64px) |
| `file_count` | Integer | Computed count of files in directory |
| `sub_directory_count` | Integer | Computed count of sub-directories |
| `parent_id` | Many2one | Parent directory (for hierarchy) |
| `visible_directory` | Boolean | Controls global visibility |
| `directory_tag_ids` | Many2many | Tags for categorizing directory |
| `attachment_ids` | One2many | Files in this directory |
| `directory_ids` | Many2many | Sub-directories (computed) |
| `files` | Integer | File count for button display |
| `sub_directories` | Integer | Sub-directory count for button display |
| `color` | Integer | Color index for UI (1-10) |
| `company_id` | Many2one | Company (multi-company support) |
| `sh_user_ids` | Many2many | Users with access to this directory |
| `sh_share_url` | Char | Shareable download link (computed) |
| `sh_access_token` | Char | Security token for shared links |

#### Key Methods

##### `default_get(fields)`
**Purpose**: Auto-populate parent directory when creating subdirectories

**Logic**:
- Checks `active_id` and `active_model` in context
- If creating from a directory view, sets that directory as parent
- Supports both direct context and params-based contexts

##### `_get_token()`
**Purpose**: Generate or retrieve access token for sharing

**Returns**: UUID string for secure access

##### `_compute_full_url()`
**Purpose**: Generate shareable download URL

**Generated URL Format**:
```
{base_url}/attachment/download_directiries?list_ids={id}&access_token={token}&name=directory
```

**Note**: Contains typo "directiries" (should be "directories")

##### `action_share_directory()`
**Purpose**: Send email with download link to specified users

**Process**:
1. Computes share URL
2. Builds comma-separated partner IDs from `sh_user_ids`
3. Sends email using template `sh_document_management_share_directory_url_template`

##### `_run_auto_delete_garbase_collection()` (cron job)
**Purpose**: Clean up temporary ZIP files

**Schedule**: Runs daily (defined in `data/ir_crom_data.xml`)

**Logic**: Deletes all attachments with `sh_document_as_zip = True`

**Note**: Contains typo "garbase" (should be "garbage")

##### `action_download_as_zip()`
**Purpose**: Export directory and files as ZIP

**Process**:
1. Creates temporary directory structure
2. Writes all attachment files to temp directory
3. Creates ZIP file in memory
4. Creates temporary attachment with ZIP
5. Returns download URL
6. Cleans up temp directory

**Implementation Details**:
- Uses `/tmp` directory (Linux-specific, may fail on Windows)
- Creates directory structure matching folder hierarchy
- Handles filename sanitization (replaces `/` with `_`)
- ZIP is marked with `sh_document_as_zip = True` for auto-deletion

##### `create(vals_list)`
**Purpose**: Auto-assign sequence and random color on creation

**Logic**:
- Gets next sequence number from `document.directory` sequence
- Assigns random color (1-10)

##### Computed Fields Methods

- `_compute_file_counts()`: Counts attachments in directory
- `_compute_sub_directory_count()`: Counts child directories
- `_compute_file_counts_btn()`: Button-specific file count
- `_compute_sub_directory_count_btn()`: Button-specific subdirectory count

##### Navigation Methods

- `action_view_sub_directory()`: Opens subdirectories view
- `action_view_files()`: Opens files view for this directory
- `action_view()`: Generic view action for files

---

### 2. document.tags

**File**: `models/document_tags.py`

Simple tag model for categorizing documents.

#### Key Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `name` | Char | Tag name (required) |
| `color` | Integer | Color index for UI (1-10) |

#### Key Methods

##### `create(vals_list)`
**Purpose**: Auto-assign random color on creation

---

### 3. directory.tags

**File**: `models/directory_tags.py`

Simple tag model for categorizing directories.

#### Key Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `name` | Char | Tag name (required) |
| `color` | Integer | Color index for UI (1-10) |

#### Key Methods

##### `create(vals_list)`
**Purpose**: Auto-assign random color on creation

---

### 4. ir.attachment (Extended)

**File**: `models/ir_attachment.py`

Extends Odoo's base attachment model with document management features.

#### Additional Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `directory_id` | Many2one | Parent directory |
| `document_tags` | Many2many | Document classification tags |
| `color` | Integer | Color index for UI (1-10) |
| `sh_document_as_zip` | Boolean | Marks temporary ZIP files |
| `sh_user_ids` | Many2many | Users with access |
| `sh_share_url` | Char | Shareable download link (computed) |

**Note**: Uses different relation name (`rel_attachment_user`) than directories to avoid conflicts

#### Key Methods

##### `_compute_full_url()`
**Purpose**: Generate shareable download URL for documents

**Generated URL Format**:
```
{base_url}/attachment/download_directiries?list_ids={id}&access_token={access_token}&name=document
```

##### `action_share_directory()`
**Purpose**: Send email with download link

**Note**: Method name is misleading (should be `action_share_document`)

##### `default_get(fields)`
**Purpose**: Auto-populate directory when creating files

**Logic**: Similar to directory model, sets directory context

##### `create(vals_list)`
**Purpose**: Auto-assign random color on creation

##### `action_download_as_zip_attachment()`
**Purpose**: Export selected attachments as ZIP

**Process**:
1. Gets selected attachments from context
2. Collects unique directories containing those attachments
3. Creates ZIP containing all files from those directories
4. Returns download URL

**Limitation**: Exports entire directories, not just selected files

##### `action_document_preview()`
**Purpose**: Preview document in browser

**Supported Types**:
- URLs (opens in new tab)
- PDFs (`application/pdf`)
- Images (JPEG, JPG, PNG)
- Text files (`text/plain`)

**Error Handling**: Raises `UserError` if preview not available

---

### 5. sh.share.directories (Transient)

**File**: `wizard/sh_share_directories.py`

Wizard model for sharing directories (appears incomplete).

#### Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `sh_name` | Char | Name field |
| `access_token` | Char | UUID for secure access (required) |
| `sh_share_url` | Char | Computed share URL |

**Status**: Model is defined but `_compute_full_url()` method is not implemented

---

## Views & UI

### Menu Structure

**File**: `views/menus.xml`

```
Documents (menu_document)
├── All Documents (menu_all_document)
│   └── All Documents (sub_menu_all_document)
├── Document Directory (directory_menu)
│   └── Directory (directory_main_menu)
└── Configuration (menu_configuration)
```

**Access**: Requires `document_group_user` group

**Icon**: Custom icon at `static/description/menu_icon.png`

---

### document.directory Views

**File**: `views/document_directory_views.xml`

#### 1. Kanban View (`directory_kanban`)

**Features**:
- Displays directory icon/image
- Shows directory name
- Two action buttons:
  - Files count (opens files view)
  - Sub-directories count (opens subdirectories view)
- Quick create enabled
- Color-coded by random color index

**Template**: Custom kanban template with image and dual button layout

#### 2. Form View (`directory_form_view`)

**Layout**:

**Header Buttons**:
- Files statbutton (opens files view)
- Sub Directories statbutton (opens subdirectories view)

**Main Content**:
- Avatar image (image_medium)
- Directory name (title)
- Parent directory selector
- File count (read-only)
- Sub-directory count (read-only)
- Directory tags (many2many_tags widget with colors)
- Share users (many2many_tags widget)
- Share URL (CopyClipboardChar widget, hidden by default)
- Share button (action_share_directory)
- Visible directory checkbox

**Notebooks**:
- **Files Tab**: List of attachments with download links
- **Sub Directories Tab**: Many2many field showing child directories

#### 3. Tree/List View (`directory_tree_view`)

**Columns**:
- Sequence (drag handle for reordering)
- Name
- "View Related Files" button

#### 4. Search View (`directory_search_view`)

**Search Fields**:
- Name
- Parent directory
- Created by user
- Create date

**Filters**:
- Visible Directory (domain: `visible_directory = True`)
- My Directory (domain: `create_uid = current user`)

**Group By Options**:
- Created By
- Parent Directory
- Create Date

**Default Filter**: Visible Directory is active by default (context: `{'search_default_visible': 1}`)

---

### ir.attachment Views

**File**: `views/ir_attachment_views.xml`

#### 1. Kanban View (`sh_document_management_kanban_view`)

**Custom Class**: `sh_documents_kanban` (JavaScript component)

**Features**:
- Document preview images (for images/PDFs)
- File type icons (for other types)
- URL display for URL-type attachments
- Created date and user avatar
- Download option in dropdown menu
- Delete option in dropdown menu

**Preview Logic**:
- Images: Shows thumbnail
- PDFs/Videos: Shows preview icon
- URLs: Shows link icon
- Other: Shows mime-type based icon

#### 2. Form View (`attachment_form_view_inherit`)

**Inherited from**: `base.view_attachment_form`

**Added Fields** (before type field):
- Directory selector
- Document tags (many2many_tags with colors)
- Share users (many2many_tags)
- Share URL (CopyClipboardChar, hidden)

**Added Elements**:
- Share button (action_share_directory method)

#### 3. Tree View (`sh_document_management_tree_view`)

**Inherited from**: `base.view_attachment_tree`

**Added After create_date**:
- Preview button (action_document_preview method)

---

### Server Actions

**File**: `views/document_directory_views.xml`

#### 1. Export Directory as ZIP (`sh_download_zip_multi_action`)

- **Model**: `document.directory`
- **Binding**: List view (multi-select)
- **Action**: Calls `action_download_as_zip()`
- **Appears**: In "Action" menu when directories are selected

#### 2. Export Attachments as ZIP (`sh_download_zip_multi_action_attachment`)

- **Model**: `ir.attachment`
- **Binding**: List view (multi-select)
- **Action**: Calls `action_download_as_zip_attachment()`
- **Appears**: In "Action" menu when attachments are selected

---

### Other View Files

**Directory Tags**: `views/directory_tags_views.xml` - Standard CRUD views for directory tags

**Document Tags**: `views/document_tags_views.xml` - Standard CRUD views for document tags

---

## Controllers & Routes

### sh_download_directories.py

**File**: `controllers/sh_download_directories.py`

**Class**: `ShDocumentCustomerPortal`

#### Route: `/attachment/download_directiries`

**URL Typo**: "directiries" should be "directories"

**Configuration**:
- **Type**: HTTP
- **Auth**: Public (accessible without login)
- **Website**: False
- **CSRF**: False (allows external access)

**Parameters**:
- `list_ids`: Directory or document ID
- `name`: Type identifier ('directory' or 'document')
- `access_token`: Security token (validated by record rules)

**Purpose**: Download directory or document as ZIP file

**Process Flow**:

1. **Validation**: Returns 404 if `list_ids` is empty

2. **Type Handling**:
   - If `name == 'directory'`:
     - Searches for attachments in that directory
     - Uses directory name for ZIP filename
   - If `name == 'document'`:
     - Searches for specific attachment
     - Uses document name (without extension) for ZIP filename

3. **ZIP Creation**:
   - Creates in-memory ZIP file
   - Iterates through attachments
   - Skips non-binary attachments
   - Uses `ir.binary._get_stream_from()` to get file content
   - Adds each file to ZIP with original name

4. **Response**:
   - Returns ZIP file as HTTP response
   - Sets appropriate headers:
     - Content-Type: zip
     - Content-Disposition: attachment with filename
     - X-Content-Type-Options: nosniff (security)

**Security Considerations**:
- Public auth means anyone with URL can download
- Access control relies on token validation
- No explicit token validation in controller (relies on record rules)

**Error Handling**:
- Catches `BadZipfile` exceptions
- Logs exceptions via `logger`

---

## Security

### Groups

**File**: `security/sh_document_management_groups.xml`

#### 1. Document Category (`module_document_category`)
- Category for all document-related groups
- Sequence: 20

#### 2. User Group (`document_group_user`)
- **Implies**: `base.group_user` (internal user)
- **Purpose**: Basic access to document management features
- **Access**: Can access own documents and shared documents

#### 3. Manager Group (`document_group_manager`)
- **Implies**: `document_group_user`
- **Purpose**: Full access to all documents
- **Default Members**: Administrator, OdooBot
- **Access**: Can access all documents regardless of ownership

---

### Access Rights

**File**: `security/ir.model.access.csv`

| Model | Group | Read | Write | Create | Delete |
|-------|-------|------|-------|--------|--------|
| document.tags | User | Yes | Yes | Yes | Yes |
| directory.tags | User | Yes | Yes | Yes | Yes |
| document.directory | User | Yes | Yes | Yes | Yes |
| sh.share.directories | User | Yes | Yes | Yes | Yes |

**Note**: All models grant full CRUD access to User group. Fine-grained control is via record rules.

---

### Record Rules

**File**: `security/sh_document_management_groups.xml`

#### 1. Directory Multi-Company Rule (`directory_comp_rule`)
- **Model**: `document.directory`
- **Global**: True
- **Domain**: `['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]`
- **Purpose**: Users can only see directories from their companies

#### 2. User Directory Access (`user_document_directory_rule`)
- **Model**: `document.directory`
- **Group**: User
- **Domain**: `['|', ('sh_user_ids', 'in', [user.id]), ('create_uid', '=', user.id)]`
- **Purpose**: Users can access:
  - Directories they created
  - Directories shared with them

#### 3. Manager Directory Access (`manager_document_directory_rule`)
- **Model**: `document.directory`
- **Group**: Manager
- **Domain**: `[(1, '=', 1)]` (always true)
- **Purpose**: Managers can access all directories

#### 4. User Attachment Access (`user_ir_attachment_rule`)
- **Model**: `ir.attachment`
- **Group**: User
- **Domain**: `['|', '|', ('sh_user_ids', 'in', [user.id]), ('create_uid', '=', user.id), ('public', '=', True)]`
- **Purpose**: Users can access:
  - Attachments they created
  - Attachments shared with them
  - Public attachments

#### 5. Manager Attachment Access (`manager_ir_attachment_rule`)
- **Model**: `ir.attachment`
- **Group**: Manager
- **Domain**: `[(1, '=', 1)]` (always true)
- **Purpose**: Managers can access all attachments

---

## Key Features

### 1. Directory Hierarchy

**Implementation**:
- Self-referential `parent_id` field on `document.directory`
- Unlimited nesting depth supported
- Breadcrumb navigation via parent chain

**UI Features**:
- Create subdirectories from parent directory form view
- Kanban view shows sub-directory count
- Dedicated "Sub Directories" tab in form view
- "View Sub Directory" action opens filtered kanban view

**Context Handling**:
- `default_get()` method auto-sets parent when creating from directory
- Works with both `active_id` and URL params

---

### 2. File Management

**Storage**:
- Files stored in Odoo's standard `ir.attachment` table
- Linked to directories via `directory_id` field
- Inherits all standard attachment features (filestore, database storage, etc.)

**Upload**:
- Upload files directly in directory form view
- Upload via "All Documents" menu
- Auto-assigns to current directory if in directory context

**Download**:
- Individual file download via attachment form/list
- Bulk download as ZIP via server action
- Shared download via public URL

**Organization**:
- Categorize with document tags (many2many)
- Filter by directory, tags, creator, date
- Search by name and metadata

---

### 3. Sharing Functionality

**Directory Sharing**:

**Process**:
1. Select users in `sh_user_ids` field
2. Click "Share" button
3. System generates access token (UUID)
4. Computes shareable URL
5. Sends email to selected users
6. Recipients can download directory as ZIP (no login required)

**Security**:
- Public route requires access token
- Token is unique per directory
- Regenerated if missing
- Recipients must have access token in URL

**Document Sharing**:
- Similar process to directory sharing
- Uses same controller with `name=document` parameter
- Downloads single document (or all in same directory)

**Email Template**:
- Defined in `data/mail_template_data.xml`
- Includes clickable download link
- Customizable message

---

### 4. ZIP Export

**Two Export Methods**:

#### A. Directory Export (`action_download_as_zip`)

**Trigger**: Server action on directory list view

**Process**:
1. Creates temp directory in `/tmp`
2. Creates subdirectory with directory name
3. Writes all attachment files to subdirectory
4. Creates ZIP from entire temp structure
5. Stores ZIP as temporary attachment (`sh_document_as_zip = True`)
6. Returns download URL
7. Cleans up temp directory

**Cleanup**: Daily cron job deletes temporary ZIP attachments

#### B. Attachment Export (`action_download_as_zip_attachment`)

**Trigger**: Server action on attachment list view

**Process**:
1. Collects unique directories of selected attachments
2. Exports all files from those directories (not just selected)
3. Similar ZIP creation process

**Limitation**: Cannot export only selected files; exports entire directories

---

### 5. Document Preview

**Trigger**: "Preview" button in attachment list view

**Method**: `action_document_preview()`

**Supported Formats**:
- **URLs**: Opens in new browser tab
- **Images**: JPEG, JPG, PNG (via `/web/content/{id}`)
- **PDFs**: Opens in browser PDF viewer
- **Text**: Plain text files

**Unsupported Formats**:
- Office documents (DOC, XLS, PPT)
- Archives (ZIP, RAR)
- Videos (requires additional configuration)

**Error Handling**: Shows user-friendly error message for unsupported types

---

### 6. Visibility Control

**Visible Directory Flag**:
- Boolean field on `document.directory`
- Filters directories in default search
- Default filter shows only visible directories
- Users can toggle "My Directory" filter to see all their directories

**Use Cases**:
- Archive old directories (set visible = False)
- Hide work-in-progress directories
- Create private vs. shared directory structure

---

### 7. Tagging System

**Two Tag Models**:

#### Directory Tags (`directory.tags`)
- Categorize folders (e.g., "Finance", "HR", "Projects")
- Many2many on directories
- Color-coded in UI

#### Document Tags (`document.tags`)
- Categorize files (e.g., "Invoice", "Contract", "Report")
- Many2many on attachments
- Color-coded in UI

**Tag Management**:
- Create via Configuration menu
- Auto-assigned random color (1-10)
- Used in many2many_tags widget (pills with colors)

---

### 8. Multi-Company Support

**Implementation**:
- `company_id` field on `document.directory`
- Default to current user's company
- Record rule enforces company isolation
- Can create company-neutral directories (`company_id = False`)

---

## JavaScript Components

### Custom Kanban View

**Files**:
- `static/src/views/sh_documents_kanban/document_management_kanban_view.js`
- `static/src/views/sh_documents_kanban/document_management_kanban_renderer.js`
- `static/src/views/sh_documents_kanban/document_management_kanban_record.js`

**Registration**:
```javascript
registry.category("views").add("sh_documents_kanban", SHDocumentKanbanView);
```

**Usage**: Applied to `ir.attachment` kanban view via `js_class="sh_documents_kanban"`

**Customizations** (likely):
- Custom drag-and-drop behavior
- Preview on hover
- Enhanced file type detection
- Custom click handlers

**Note**: Renderer and record files not analyzed in detail; would need to read to understand full functionality.

---

## Development Guidelines

### Extending the Module

#### Adding New Document Types

1. **Extend ir.attachment**:
   ```python
   class IrAttachment(models.Model):
       _inherit = 'ir.attachment'

       custom_field = fields.Char('Custom Field')
   ```

2. **Update views**: Add fields to form/kanban views

3. **Update security**: Add access rules if needed

#### Creating Custom Filters

1. **Add to search view**:
   ```xml
   <filter string="My Filter" name="my_filter"
           domain="[('field', '=', value)]"/>
   ```

2. **Reference in action**: `context="{'search_default_my_filter': 1}"`

#### Customizing ZIP Export

**Override** `action_download_as_zip()` in `document.directory`:

```python
@api.model
def action_download_as_zip(self):
    # Custom logic here
    result = super().action_download_as_zip()
    # Post-processing
    return result
```

**Considerations**:
- Handle temp directory cleanup
- Consider Windows compatibility (`/tmp` is Linux-specific)
- Mark ZIP files with `sh_document_as_zip = True` for auto-cleanup

#### Adding Email Templates

1. **Create template**: `data/custom_mail_template.xml`
2. **Reference in method**: `self.env.ref('module.template_id')`
3. **Update manifest**: Add to `data` list

---

### Testing Instructions

#### Manual Testing Checklist

**Directory Management**:
- [ ] Create top-level directory
- [ ] Create subdirectory from parent form view
- [ ] Upload image to directory
- [ ] Verify file count updates
- [ ] Verify sub-directory count updates
- [ ] Test drag-and-drop reordering in list view

**File Operations**:
- [ ] Upload various file types (PDF, image, text, office docs)
- [ ] Download individual file
- [ ] Preview PDF in browser
- [ ] Preview image in browser
- [ ] Verify preview error for unsupported types

**Tagging**:
- [ ] Create directory tag
- [ ] Create document tag
- [ ] Assign tags to directory
- [ ] Assign tags to document
- [ ] Verify color randomization

**Sharing**:
- [ ] Add users to directory `sh_user_ids`
- [ ] Click "Share" button
- [ ] Verify email sent to users
- [ ] Copy share URL
- [ ] Open share URL in incognito browser (test public access)
- [ ] Verify ZIP download works without login
- [ ] Test invalid token (should fail)

**ZIP Export**:
- [ ] Select multiple directories in list view
- [ ] Choose "Export as zip" from Action menu
- [ ] Verify ZIP downloads correctly
- [ ] Extract and verify files are intact
- [ ] Repeat for attachments

**Security**:
- [ ] Login as User (non-manager)
- [ ] Verify user only sees own directories
- [ ] Verify user sees shared directories
- [ ] Login as Manager
- [ ] Verify manager sees all directories

**Multi-Company** (if applicable):
- [ ] Create directory in Company A
- [ ] Switch to Company B
- [ ] Verify Company A directory is hidden
- [ ] Create company-neutral directory (`company_id = False`)
- [ ] Verify visible in both companies

#### Automated Testing Template

```python
from odoo.tests import TransactionCase

class TestDocumentManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Directory = self.env['document.directory']
        self.Attachment = self.env['ir.attachment']

    def test_directory_creation(self):
        """Test directory creation with auto-sequence"""
        directory = self.Directory.create({'name': 'Test Dir'})
        self.assertTrue(directory.sequence > 0)
        self.assertTrue(1 <= directory.color <= 10)

    def test_subdirectory_context(self):
        """Test subdirectory auto-parent"""
        parent = self.Directory.create({'name': 'Parent'})
        child = self.Directory.with_context(
            active_id=parent.id,
            active_model='document.directory'
        ).create({'name': 'Child'})
        self.assertEqual(child.parent_id, parent)

    def test_file_count(self):
        """Test file count computation"""
        directory = self.Directory.create({'name': 'Test Dir'})
        self.assertEqual(directory.file_count, 0)

        self.Attachment.create({
            'name': 'test.txt',
            'directory_id': directory.id,
            'datas': 'test content'
        })
        self.assertEqual(directory.file_count, 1)
```

---

### Common Patterns Used

#### 1. Context-Based Defaults

**Pattern**: `default_get()` reads context to auto-populate fields

**Used In**:
- `document.directory.default_get()` - auto-set parent
- `ir.attachment.default_get()` - auto-set directory

**Example**:
```python
@api.model
def default_get(self, fields):
    rec = super().default_get(fields)
    if self._context.get('active_model') == 'document.directory':
        rec['directory_id'] = self._context.get('active_id')
    return rec
```

#### 2. Computed Share URLs

**Pattern**: Generate URLs with tokens for public access

**Used In**:
- `document.directory._compute_full_url()`
- `ir.attachment._compute_full_url()`

**Example**:
```python
def _compute_full_url(self):
    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    self.sh_share_url = f"{base_url}/path?id={self.id}&token={self._get_token()}"
```

#### 3. Server Actions for Batch Operations

**Pattern**: Use `ir.actions.server` for multi-record operations

**Used In**:
- Export directories as ZIP
- Export attachments as ZIP

**Definition**:
```xml
<record id="action_id" model="ir.actions.server">
    <field name="name">Action Name</field>
    <field name="model_id" ref="model_reference"/>
    <field name="binding_model_id" ref="model_reference"/>
    <field name="state">code</field>
    <field name="binding_view_types">list</field>
    <field name="code">action = model.method_name()</field>
</record>
```

#### 4. Temporary File Cleanup via Cron

**Pattern**: Mark temporary records with flag, clean up via scheduled action

**Used In**: ZIP file cleanup

**Cron Definition**:
```xml
<record id="cron_id" model="ir.cron">
    <field name="name">Cleanup Job</field>
    <field name="interval_type">days</field>
    <field name="interval_number">1</field>
    <field name="model_id" ref="model_reference"/>
    <field name="code">model._cleanup_method()</field>
</record>
```

#### 5. UUID Access Tokens

**Pattern**: Generate UUID for secure public access

**Used In**: Directory and document sharing

**Example**:
```python
import uuid

sh_access_token = fields.Char("Access Token")

def _get_token(self):
    if not self.sh_access_token:
        self.sh_access_token = str(uuid.uuid4())
    return self.sh_access_token
```

---

## Known Issues & TODOs

### Critical Issues

#### 1. URL Typo in Route Definition

**Location**: `controllers/sh_download_directories.py:14`

**Issue**: Route is `/attachment/download_directiries` (should be `directories`)

**Impact**:
- All generated share URLs use this typo
- Changing it will break existing shared links
- Inconsistent with model/field naming

**Fix Recommendation**:
```python
# Option A: Fix typo and add redirect for old URLs
@http.route(['/attachment/download_directories'], ...)
def sh_download_directories(self, ...):
    ...

@http.route(['/attachment/download_directiries'], ...)  # Deprecated
def sh_download_directiries_deprecated(self, **kwargs):
    return self.sh_download_directories(**kwargs)

# Option B: Keep typo, add comment explaining why
@http.route(['/attachment/download_directiries'], ...)  # Note: Typo in URL is intentional for backward compatibility
def sh_download_directiries(self, ...):
    ...
```

#### 2. Temporary Directory Hardcoded to `/tmp`

**Location**: `models/document_directory.py:123` and `models/ir_attachment.py:93`

**Issue**: Uses Linux-specific `/tmp` directory

**Impact**: Will fail on Windows systems

**Fix Recommendation**:
```python
import tempfile

# Replace:
path_main = os.path.join('/tmp')

# With:
path_main = tempfile.gettempdir()  # Cross-platform temp directory
```

#### 3. Typo: "Garbase" Collection

**Location**:
- `models/document_directory.py:109` - method name
- `data/ir_crom_data.xml:4` - cron name

**Issue**: Should be "Garbage"

**Impact**: Confusing method/cron naming

**Fix Recommendation**:
```python
# Rename method
def _run_auto_delete_garbage_collection(self):
    ...

# Update cron XML
<field name="name">Delete Garbage Collection</field>
<field name="code">model._run_auto_delete_garbage_collection()</field>
```

#### 4. Typo: "Diractory" in Field String

**Location**: `models/document_directory.py:34`

**Issue**: Field label is "Diractory Tags" (should be "Directory Tags")

**Impact**: UI displays incorrect label

**Fix**:
```python
directory_tag_ids = fields.Many2many('directory.tags', string='Directory Tags')
```

---

### Functional Issues

#### 5. Incomplete Wizard Model

**Location**: `wizard/sh_share_directories.py`

**Issue**:
- Model defined with fields
- `_compute_full_url()` method referenced but not implemented
- No views defined
- Not used anywhere in module

**Impact**: Dead code in codebase

**Fix Options**:
- Implement wizard functionality (if needed)
- Remove wizard entirely (if not needed)

#### 6. ZIP Export Exports Entire Directories

**Location**: `models/ir_attachment.py:78-137`

**Issue**: `action_download_as_zip_attachment()` exports all files from directories, not just selected attachments

**Expected Behavior**: Should export only selected files

**Current Behavior**:
1. User selects 3 files from different directories
2. System exports ALL files from those 3 directories

**Fix Recommendation**:
```python
def action_download_as_zip_attachment(self):
    if self.env.context.get('active_ids'):
        attachment_ids = self.env['ir.attachment'].sudo().browse(
            self.env.context.get('active_ids'))

        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for attachment in attachment_ids:  # Only selected attachments
                attachment_name = attachment.name.replace('/', '_') if attachment.name else 'attachment'
                content_base64 = base64.b64decode(attachment.datas)
                zf.writestr(attachment_name, content_base64)

        # Return ZIP...
```

#### 7. Missing Access Token Validation in Controller

**Location**: `controllers/sh_download_directories.py:14-63`

**Issue**: Controller is public but doesn't explicitly validate access token

**Security Risk**: Relies on record rules, but doesn't verify token matches record

**Fix Recommendation**:
```python
def sh_download_directiries(self, list_ids='', access_token='', name='', **post):
    if not list_ids or not access_token:
        return request.not_found()

    # Validate token
    if name == 'directory':
        directory = request.env['document.directory'].sudo().browse(int(list_ids))
        if not directory.exists() or directory.sh_access_token != access_token:
            return request.not_found()

    # ... rest of logic
```

#### 8. Cron XML File Typo

**Location**: `data/ir_crom_data.xml` (filename)

**Issue**: Filename is "crom" instead of "cron"

**Impact**: Confusing filename

**Fix**: Rename file to `ir_cron_data.xml`

---

### Enhancements / TODOs

#### 9. Add Breadcrumb Navigation

**Feature**: Show directory path in form view

**Implementation**:
```python
directory_path = fields.Char('Path', compute='_compute_directory_path')

@api.depends('name', 'parent_id')
def _compute_directory_path(self):
    for rec in self:
        path = rec.name
        parent = rec.parent_id
        while parent:
            path = f"{parent.name} / {path}"
            parent = parent.parent_id
        rec.directory_path = path
```

#### 10. Add File Size Field

**Feature**: Display total size of files in directory

**Implementation**:
```python
total_size = fields.Float('Total Size (MB)', compute='_compute_total_size')

@api.depends('attachment_ids.file_size')
def _compute_total_size(self):
    for rec in self:
        total_bytes = sum(rec.attachment_ids.mapped('file_size'))
        rec.total_size = total_bytes / (1024 * 1024)  # Convert to MB
```

#### 11. Add Directory Move/Copy Actions

**Feature**: Move/copy directories between parents

**Implementation**: Wizard to select new parent, update `parent_id` field

#### 12. Add Duplicate File Detection

**Feature**: Warn when uploading duplicate file (same checksum)

**Implementation**:
```python
@api.constrains('datas', 'directory_id')
def _check_duplicate_file(self):
    for rec in self:
        if rec.checksum:
            duplicate = self.search([
                ('id', '!=', rec.id),
                ('checksum', '=', rec.checksum),
                ('directory_id', '=', rec.directory_id.id)
            ], limit=1)
            if duplicate:
                raise ValidationError(f"File with same content already exists: {duplicate.name}")
```

#### 13. Add Trash/Recycle Bin

**Feature**: Soft-delete directories and files

**Implementation**:
```python
active = fields.Boolean(default=True)
deleted_date = fields.Datetime()

def action_delete(self):
    self.write({'active': False, 'deleted_date': fields.Datetime.now()})
```

#### 14. Add Version Control for Documents

**Feature**: Track document versions

**Implementation**: New model `document.version` linking to `ir.attachment`

#### 15. Add Full-Text Search

**Feature**: Search within document content

**Implementation**: Integrate with `ir.attachment` indexing capabilities

---

### Code Quality Improvements

#### 16. Extract Duplicate ZIP Logic

**Issue**: ZIP creation logic duplicated in two methods

**Fix**: Extract to common method
```python
def _create_zip_from_attachments(self, attachment_ids, zip_name='Documents.zip'):
    """Common method for ZIP creation"""
    mem_zip = BytesIO()
    # ... ZIP logic ...
    return get_attachment.id
```

#### 17. Add Type Hints (Python 3.5+)

**Enhancement**: Add type hints for better IDE support

**Example**:
```python
from typing import List, Dict, Any

def action_download_as_zip(self) -> Dict[str, Any]:
    ...
```

#### 18. Add Docstrings

**Enhancement**: Add comprehensive docstrings to all methods

**Example**:
```python
def action_download_as_zip(self):
    """
    Export selected directories and their contents as a ZIP file.

    Returns:
        dict: Action dictionary to trigger ZIP download

    Raises:
        UserError: If no directories are selected
    """
    ...
```

---

## Conclusion

This document provides a comprehensive overview of the `sh_document_management` module. For questions or support, contact:

- **Email**: support@softhealer.com
- **Website**: https://softhealer.com
- **Blog**: https://www.softhealer.com/blog/odoo-2/post/document-management-487

---

**Document Version**: 1.0
**Last Updated**: 2025-12-08
**Module Version**: 0.0.1
**Odoo Version**: 18.0
