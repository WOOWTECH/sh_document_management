# PRD: sh_document_management Module Code Review

## Document Information
- **Module**: sh_document_management
- **Version**: 0.1.0
- **Date**: 2026-02-17
- **Review Type**: Comprehensive Code Review

---

## 1. Module Overview

### 1.1 Purpose
Odoo 18 文件管理系統，提供階層式目錄結構、檔案上傳/下載/預覽、公開分享連結、ZIP 匯出等功能。

### 1.2 Core Features
- **目錄管理**: 階層式目錄結構，支援無限層級巢狀
- **檔案管理**: 上傳、下載、預覽、標籤分類
- **公開分享**: Token-based 公開下載連結，無需登入
- **ZIP 匯出**: 批量匯出目錄或選定檔案為 ZIP
- **權限控制**: 使用者/管理員群組，多公司隔離
- **自動偵測**: 公開 URL 自動偵測，HTTPS 強制轉換

---

## 2. Architecture

### 2.1 Models
| Model | File | Description |
|-------|------|-------------|
| `document.directory` | `models/document_directory.py` | 主要目錄模型，階層結構 |
| `ir.attachment` (extended) | `models/ir_attachment.py` | 擴展 Odoo 附件模型 |
| `document.tags` | `models/document_tags.py` | 文件標籤 |
| `directory.tags` | `models/directory_tags.py` | 目錄標籤 |
| `ir.config_parameter` (extended) | `models/ir_config_parameter.py` | 公開 URL 偵測 |

### 2.2 Controllers
| Route | File | Auth | Purpose |
|-------|------|------|---------|
| `/attachment/download_directories` | `controllers/sh_download_directories.py` | Public | Token-protected 下載 |

### 2.3 Frontend Components
| Component | File | Purpose |
|-----------|------|---------|
| `SHDocumentKanbanView` | `static/src/views/sh_documents_kanban/` | 自訂看板視圖 |
| `SHDocumentKanbanRenderer` | 同上 | 自訂渲染器 |
| `SHDocumentKanbanRecord` | 同上 | 檔案預覽整合 |

### 2.4 Security
- **Groups**: `document_group_user`, `document_group_manager`
- **Record Rules**: 公司隔離、使用者存取、管理員全權
- **Token Validation**: UUID access_token 驗證

---

## 3. Code Review Criteria

### 3.1 Code Quality
- [ ] PEP 8 / Odoo coding standards compliance
- [ ] Proper error handling
- [ ] Code documentation (docstrings, comments)
- [ ] DRY principles (no code duplication)
- [ ] Naming conventions

### 3.2 Security
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Access token validation
- [ ] File upload security
- [ ] Path traversal prevention
- [ ] Privilege escalation checks

### 3.3 Performance
- [ ] Query optimization (N+1 queries)
- [ ] Proper use of computed fields
- [ ] Large file handling
- [ ] Memory management (ZIP creation)
- [ ] Database index usage

### 3.4 Odoo Best Practices
- [ ] Model inheritance patterns
- [ ] View inheritance patterns
- [ ] API decorator usage (@api.depends, @api.model, etc.)
- [ ] Recordset handling
- [ ] Transaction management
- [ ] Multi-company support

### 3.5 Frontend (JavaScript)
- [ ] OWL component patterns
- [ ] Proper imports/exports
- [ ] Error handling
- [ ] Memory leaks prevention
- [ ] Accessibility (a11y)

### 3.6 Maintainability
- [ ] Module structure
- [ ] Dependency management
- [ ] Migration path
- [ ] Test coverage potential

---

## 4. Known Issues (from CHANGELOG)

### 4.1 Fixed in v0.1.0
| Issue | Description | Status |
|-------|-------------|--------|
| BUG-001 | Kanban 下載按鈕無效 | Fixed |
| BUG-002 | 分享 URL 使用內網 IP | Fixed |
| BUG-003 | 分享郵件接收者混亂 | Fixed |
| BUG-004 | 未選擇使用者時報錯 | Fixed |
| BUG-005 | ZIP 匯出包含整個目錄 | Fixed |
| FIX-006 | 強制 HTTPS for public URLs | Fixed |

### 4.2 Potential Concerns
- Legacy route typo (`download_directiries`) maintained for compatibility
- Wizard model removed but ACL entry may still exist
- CSRF disabled on public route (intentional for external access)

---

## 5. Test Scenarios

### 5.1 Functional Tests
1. 建立階層目錄結構
2. 上傳各種檔案類型
3. 預覽 PDF、圖片、文字檔
4. 下載單一檔案
5. ZIP 匯出目錄
6. ZIP 匯出選定檔案
7. 公開分享連結功能
8. 標籤管理

### 5.2 Security Tests
1. 未授權使用者存取
2. 無效 token 拒絕
3. 跨公司資料隔離
4. 檔案路徑注入測試

### 5.3 Performance Tests
1. 大量檔案目錄效能
2. 大檔案 ZIP 匯出
3. 多使用者並發存取

---

## 6. Review Output Format

Code review 應產出：
1. **Issues List**: 按嚴重程度分類 (Critical/High/Medium/Low)
2. **Recommendations**: 改善建議
3. **Positive Findings**: 良好實踐
4. **Action Items**: 具體修改項目

---

## Appendix: File Structure

```
sh_document_management/
├── __init__.py
├── __manifest__.py
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── models/
│   ├── __init__.py
│   ├── document_directory.py
│   ├── ir_attachment.py
│   ├── document_tags.py
│   ├── directory_tags.py
│   └── ir_config_parameter.py
├── controllers/
│   ├── __init__.py
│   └── sh_download_directories.py
├── views/
│   ├── menus.xml
│   ├── document_directory_views.xml
│   ├── ir_attachment_views.xml
│   ├── document_tags_views.xml
│   └── directory_tags_views.xml
├── security/
│   ├── sh_document_management_groups.xml
│   └── ir.model.access.csv
├── data/
│   ├── ir_cron_data.xml
│   └── mail_template_data.xml
├── static/
│   ├── description/
│   └── src/views/sh_documents_kanban/
│       ├── document_management_kanban_view.js
│       ├── document_management_kanban_renderer.js
│       └── document_management_kanban_record.js
└── wizard/
    └── __init__.py
```
