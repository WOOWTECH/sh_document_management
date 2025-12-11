# Document Management for Odoo 18 : sh_document_management

A comprehensive document management system for Odoo 18 that enables organizations to organize, share, and manage files in hierarchical directory structures.

## Overview

**Document Management** provides a centralized repository for all your organization's files within Odoo. Replace scattered file storage across emails and external drives with an organized, permission-controlled document system.

**Ideal for:**
- Organizations needing centralized document repositories
- Multi-location or distributed teams
- Companies using Odoo as their central platform
- Teams requiring secure document sharing without external services

## Key Features

- **Hierarchical Directories** - Create nested folder structures with unlimited depth for intuitive organization
- **File Management** - Upload, organize, and download documents of any file type
- **Tagging System** - Color-coded tags for categorizing both directories and documents
- **Secure Sharing** - Share directories or files via email with secure public download links (no login required)
- **Bulk ZIP Export** - Download entire directories or selected files as compressed ZIP archives
- **Document Preview** - Preview PDFs, images, and text files directly in the browser
- **Access Control** - Fine-grained permissions with User and Manager roles

## Requirements

| Requirement | Version |
|-------------|---------|
| Odoo | 18.0 |
| Python | 3.10+ |

### Dependencies
This module depends only on core Odoo modules:
- `base` - Core Odoo framework
- `mail` - Email functionality for sharing
- `web` - Web interface components

No external Python packages required.

## Installation

### Step

1. Copy the module sh_document_management to your odoo server. If you use Samba Share, copy to path `\addon_configs\local_odoo\odoo_custom_addons`.
2. Restart odoo. You can restart odoo in HomeAssistant addon.
3. Install module
   - Go to **Apps** menu in Odoo
   - Click **Update Apps List** (enable Developer Mode if not visible)
   - Search for "sh_document_management"
   - Click **Install**

## Initial Setup

After installation, complete these steps:

### 1. Assign User Permissions

Navigate to **Settings > Users & Companies > Users** and assign one of:

| Group | Access Level |
|-------|--------------|
| Document > User | Access own documents and shared documents |
| Document > Manager | Full access to all documents |

### 2. Create Tags (Optional)

Organize your documents with tags:

1. Go to **Documents > Configuration > Directory Tags**
   - Create tags like "Finance", "HR", "Projects"

2. Go to **Documents > Configuration > Document Tags**
   - Create tags like "Invoice", "Contract", "Report"

### 3. Configure Public URL (Recommended)

For sharing to work correctly over the internet:

1. Log into Odoo using your **public URL** (e.g., `https://odoo.yourcompany.com`)
2. The system automatically detects and saves this URL for share links
3. All share links will now use the public URL instead of local IP addresses

## User Guide

### Creating Directories

1. Navigate to **Documents > Document Directory**
2. Click **Create** or use the quick-create feature in kanban view
3. Fill in:
   - **Name** - Directory name
   - **Parent Directory** - Select parent for nested structure (optional)
   - **Directory Tags** - Add category tags (optional)
   - **Visible Directory** - Uncheck to hide from default view

**Tip:** Create subdirectories directly from a parent directory's form view - the parent is automatically set.

### Uploading Files

**From Directory View:**
1. Open a directory
2. Go to the **Files** tab
3. Click **Add a line** to upload files

**From All Documents:**
1. Navigate to **Documents > All Documents**
2. Click **Create**
3. Select a **Directory** and upload your file

### Organizing with Tags

**Tag Directories:**
1. Open a directory form
2. Add tags in the **Directory Tags** field
3. Tags appear as colored pills for easy identification

**Tag Documents:**
1. Open a document form
2. Add tags in the **Document Tags** field
3. Use tags to filter and group documents

### Sharing Documents

**Share a Directory:**
1. Open the directory you want to share
2. Add recipients in the **Share Users** field
3. Click the **Share** button
4. Recipients receive an email with a download link
5. The link downloads all files as a ZIP (no login required)

**Share a Single Document:**
1. Open the document form
2. Add recipients in **Share Users**
3. Click **Share**
4. Recipients can download the file directly

**Copy Share URL:**
- The **Share URL** field shows the public download link
- Click the copy icon to copy the URL manually

### Downloading and Exporting

**Download Individual Files:**
- Click the download button on any document

**Bulk Export as ZIP:**
1. Go to directory or document list view
2. Select multiple items using checkboxes
3. Click **Action > Export as zip**
4. Download the generated ZIP file

**Download Shared Directory:**
- Recipients click the link in the share email
- Entire directory downloads as ZIP automatically

### Previewing Documents

Preview supported documents without downloading:

1. Open the document list view
2. Click the **Preview** button on any document

**Supported Formats:**
| Format | Preview Type |
|--------|--------------|
| PDF | Browser PDF viewer |
| JPEG, JPG, PNG | Image viewer |
| Text files | Text display |
| URLs | Opens in new tab |

**Note:** Office documents (DOC, XLS, PPT) are not supported for preview - download to view.

## Access Control

### User Permissions

| Feature | User | Manager |
|---------|------|---------|
| Create directories | Yes | Yes |
| Create documents | Yes | Yes |
| View own directories | Yes | Yes |
| View shared directories | Yes | Yes |
| View ALL directories | No | Yes |
| Share directories | Yes | Yes |
| Export as ZIP | Yes | Yes |
| Access Configuration | No | Yes |

### Visibility Control

- **Visible Directory** checkbox controls global visibility
- Hidden directories remain accessible to their creators
- Use "My Directory" filter to see your hidden directories

## Troubleshooting

### Share links don't work externally

**Problem:** Share URLs use internal IP addresses.

**Solution:** Log into Odoo using your public URL (e.g., `https://odoo.yourcompany.com`). The system will automatically detect and use this for share links.

### Cannot preview document

**Problem:** Preview shows error message.

**Solution:** Preview only supports PDFs, images (JPEG, PNG), and text files. Download other file types to view them.

### Temporary ZIP files accumulating

**Problem:** Disk space increasing from ZIP exports.

**Solution:** A daily cron job automatically cleans temporary ZIP files. Verify the scheduled action is active at **Settings > Technical > Scheduled Actions**.

### User cannot see shared directory

**Problem:** User was added to share list but cannot see directory.

**Solution:**
1. Verify user has "Document > User" group assigned
2. Check the "Visible Directory" checkbox is enabled
3. Ensure user is correctly added to "Share Users" field

## Technical Information

| Property | Value |
|----------|-------|
| Technical Name | `sh_document_management` |
| Category | Document Management |
| Application | Yes |
| Auto-install | No |

### Models

- `document.directory` - Directory/folder structure
- `document.tags` - Document classification tags
- `directory.tags` - Directory classification tags
- `ir.attachment` (extended) - File management with directory support