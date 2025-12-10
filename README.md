About
============
This module helps to manage documents easily in odoo. You can create the directory and manage directory wise documents. Users can filter the documents by visible directory & my directory. You can easily group by the documents by directory, custom date & created by. You can easily add custom filters/groups of documents. From the menu bar, the user can see directory tags & document tags. Using a search bar you can search documents details easily. You can download the document from the files in the directory. You can see related documents from the sub-directory.

User Guide
============
Blog: https://www.softhealer.com/blog/odoo-2/post/document-management-487


Installation
============
1) Copy module files to addon folder.
2) Restart odoo service (sudo service odoo-server restart).
3) Go to your odoo instance and open apps (make sure to activate debug mode).
4) Click on update app list.
5) Search module name and hit install button.

Public URL Configuration (IMPORTANT)
=====================================
This module includes an auto-detection system for public share URLs. When you share documents or directories via email, the download links will use a publicly accessible URL instead of internal IP addresses.

**REQUIRED: Admin Login via Public URL**

After installation or upgrade, you MUST log in to your admin account at least once using the remote/public URL (e.g., `https://your-domain.com`) to trigger the auto-detection.

How it works:
1. When an admin logs in, Odoo updates the `web.base.url` system parameter
2. This module monitors `web.base.url` changes and detects public domains
3. Public URLs are automatically saved to `sh_document_management.public_base_url`
4. All share links will use this saved public URL, even if admin later logs in via local IP

Example:
- Public URL: `https://odoo.your-company.com`
- Local URL: `http://192.168.1.100:8069`
- After logging in via public URL, share links will always use `https://odoo.your-company.com`

Verification:
1. Go to Settings → Technical → Parameters → System Parameters
2. Search for `sh_document_management.public_base_url`
3. Verify it shows your public URL with `https://` prefix

Note: The module automatically forces HTTPS for public URLs to ensure compatibility with reverse proxies like Cloudflare, Nginx, etc.

Any Problem with module?
=====================================
Please create your ticket here https://softhealer.com/support

Softhealer Technologies Doubt/Inquiry/Sales/Customization Team
=====================================
Skype: live:softhealertechnologies
What's app: +917984575681
E-Mail: support@softhealer.com
Website: https://softhealer.com
