# PRD: Portal User 文件分享功能

## Document Information
- **Module**: sh_document_management
- **Feature**: Portal User Document Sharing
- **Version**: 0.3.0
- **Date**: 2026-02-17
- **Status**: Draft

---

## 1. 功能概述

### 1.1 目標
在 `sh_document_management` 模組新增 Portal User 分享功能，讓外部聯絡人（客戶、合作夥伴）可以在 Portal 頁面檢視、預覽和下載分享給他們的文件。

### 1.2 使用者故事
- **作為** 內部使用者，**我想要** 在目錄或檔案表單中選擇 Portal 使用者，**以便** 分享文件給外部聯絡人
- **作為** Portal 使用者，**我想要** 在「我的帳戶」中看到分享給我的文件，**以便** 檢視和下載

### 1.3 設計原則
- 類似 Odoo 專案/任務的架構（目錄 = 專案，檔案 = 任務）
- 目錄權限自動繼承給子目錄和檔案
- 符合 Odoo Portal 慣例

---

## 2. 功能規格

### 2.1 資料模型變更

#### 2.1.1 document.directory 模型
```python
# 新增欄位
portal_user_ids = fields.Many2many(
    'res.partner',
    relation='rel_directory_portal_user',
    string='Portal Users',
    domain="[('is_company', '=', False)]",
    help="Portal users who can access this directory and its contents"
)
```

#### 2.1.2 ir.attachment 模型（擴展）
```python
# 新增欄位
portal_user_ids = fields.Many2many(
    'res.partner',
    relation='rel_attachment_portal_user',
    string='Portal Users',
    domain="[('is_company', '=', False)]",
    help="Portal users who can directly access this file"
)
```

### 2.2 權限繼承邏輯

```
目錄 A (portal_user_ids: [Partner X, Partner Y])
├── 子目錄 A1 (繼承: Partner X, Partner Y 可存取)
│   └── 檔案 A1-1 (繼承: Partner X, Partner Y 可存取)
├── 檔案 A-1 (繼承: Partner X, Partner Y 可存取)
└── 檔案 A-2 (portal_user_ids: [Partner Z]) → Partner X, Y, Z 都可存取
```

**存取規則：**
- Portal 使用者可以存取：
  1. 直接分享給他的目錄
  2. 直接分享給他的檔案
  3. 分享給他的目錄下的所有子目錄和檔案（繼承）

### 2.3 Portal 頁面規格

#### 2.3.1 URL 路由
| 路由 | 說明 |
|------|------|
| `/my/documents` | 主頁面 - 顯示目錄和檔案列表 |
| `/my/documents/directory/<int:directory_id>` | 目錄內容頁面 |
| `/my/documents/file/<int:file_id>/preview` | 檔案預覽 |
| `/my/documents/file/<int:file_id>/download` | 檔案下載 |
| `/my/documents/directory/<int:directory_id>/download` | 目錄 ZIP 下載 |

#### 2.3.2 主頁面 (`/my/documents`) 版面配置

```
┌─────────────────────────────────────────────────────────┐
│  我的文件                                    [麵包屑導航] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  我的目錄 (3)                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │ 📁       │ │ 📁       │ │ 📁       │                │
│  │ 專案文件  │ │ 合約文件  │ │ 報價單    │                │
│  │ 5 個檔案  │ │ 3 個檔案  │ │ 2 個檔案  │                │
│  │ [進入]    │ │ [進入]    │ │ [進入]    │                │
│  └──────────┘ └──────────┘ └──────────┘                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  我的檔案 (2)                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📄 產品規格書.pdf    2026-02-15  [預覽] [下載]   │   │
│  │ 📄 報價單_v2.xlsx    2026-02-10  [下載]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 2.3.3 目錄內容頁面 (`/my/documents/directory/<id>`)

```
┌─────────────────────────────────────────────────────────┐
│  我的文件 > 專案文件                        [下載全部]   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  子目錄 (1)                                             │
│  ┌──────────┐                                          │
│  │ 📁       │                                          │
│  │ 設計稿    │                                          │
│  │ 3 個檔案  │                                          │
│  │ [進入]    │                                          │
│  └──────────┘                                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  檔案 (5)                                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📄 需求規格.pdf      2026-02-15  [預覽] [下載]   │   │
│  │ 🖼️ 架構圖.png        2026-02-14  [預覽] [下載]   │   │
│  │ 📄 會議記錄.docx     2026-02-13  [下載]          │   │
│  │ 📊 預算表.xlsx       2026-02-12  [下載]          │   │
│  │ 📦 資料包.zip        2026-02-11  [下載]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.4 支援的預覽格式

| 類型 | MIME Types | 預覽方式 |
|------|-----------|---------|
| PDF | application/pdf | 瀏覽器內嵌 PDF viewer |
| 圖片 | image/jpeg, image/png, image/gif, image/webp | 直接顯示 |
| 文字 | text/plain | 純文字顯示 |
| 其他 | - | 僅提供下載 |

### 2.5 Backend 表單介面變更

#### 2.5.1 目錄表單 (document.directory)
```xml
<!-- 在 sh_user_ids 欄位後新增 -->
<field name="portal_user_ids" widget="many2many_tags"
       options="{'color_field': 'color'}"
       placeholder="選擇 Portal 使用者..."/>
```

#### 2.5.2 檔案表單 (ir.attachment)
```xml
<!-- 在 sh_user_ids 欄位後新增 -->
<field name="portal_user_ids" widget="many2many_tags"
       options="{'color_field': 'color'}"
       placeholder="選擇 Portal 使用者..."/>
```

---

## 3. 技術架構

### 3.1 檔案結構

```
sh_document_management/
├── controllers/
│   ├── __init__.py
│   ├── sh_download_directories.py  # 現有
│   └── portal.py                   # 新增 - Portal 控制器
├── models/
│   ├── __init__.py
│   ├── document_directory.py       # 修改 - 新增 portal_user_ids
│   └── ir_attachment.py            # 修改 - 新增 portal_user_ids
├── views/
│   ├── document_directory_views.xml # 修改 - 新增欄位到表單
│   ├── ir_attachment_views.xml      # 修改 - 新增欄位到表單
│   └── portal_templates.xml         # 新增 - Portal 頁面模板
├── security/
│   ├── ir.model.access.csv          # 修改 - Portal 存取權限
│   └── sh_document_management_groups.xml # 修改 - Portal 規則
└── __manifest__.py                  # 修改 - 新增依賴和資料檔
```

### 3.2 新增依賴

```python
# __manifest__.py
"depends": ["base", "mail", "web", "portal"],  # 新增 portal
```

### 3.3 Controller 設計

```python
# controllers/portal.py
class DocumentPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """在 Portal 首頁顯示文件計數"""

    @route('/my/documents', auth='user', website=True)
    def portal_my_documents(self):
        """主頁面 - 顯示分享的目錄和檔案"""

    @route('/my/documents/directory/<int:directory_id>', auth='user', website=True)
    def portal_directory_content(self, directory_id):
        """目錄內容頁面"""

    @route('/my/documents/file/<int:file_id>/preview', auth='user', website=True)
    def portal_file_preview(self, file_id):
        """檔案預覽"""

    @route('/my/documents/file/<int:file_id>/download', auth='user', website=True)
    def portal_file_download(self, file_id):
        """檔案下載"""

    @route('/my/documents/directory/<int:directory_id>/download', auth='user', website=True)
    def portal_directory_download(self, directory_id):
        """目錄 ZIP 下載"""
```

### 3.4 存取權限檢查邏輯

```python
def _check_portal_access(self, record, record_type='directory'):
    """檢查 Portal 使用者是否有權限存取

    Args:
        record: document.directory 或 ir.attachment 記錄
        record_type: 'directory' 或 'attachment'

    Returns:
        bool: True 如果有權限
    """
    partner = request.env.user.partner_id

    if record_type == 'directory':
        # 檢查直接分享
        if partner in record.portal_user_ids:
            return True
        # 檢查父目錄繼承
        parent = record.parent_id
        while parent:
            if partner in parent.portal_user_ids:
                return True
            parent = parent.parent_id
        return False

    elif record_type == 'attachment':
        # 檢查直接分享
        if partner in record.portal_user_ids:
            return True
        # 檢查所屬目錄
        if record.directory_id:
            return self._check_portal_access(record.directory_id, 'directory')
        return False
```

### 3.5 Security Rules

```xml
<!-- Portal 使用者目錄存取規則 -->
<record id="portal_document_directory_rule" model="ir.rule">
    <field name="name">Portal: Access shared directories</field>
    <field name="model_id" ref="model_document_directory"/>
    <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="False"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_unlink" eval="False"/>
    <field name="domain_force">[
        '|',
        ('portal_user_ids', 'in', [user.partner_id.id]),
        ('parent_id.portal_user_ids', 'in', [user.partner_id.id])
    ]</field>
</record>

<!-- Portal 使用者檔案存取規則 -->
<record id="portal_ir_attachment_rule" model="ir.rule">
    <field name="name">Portal: Access shared attachments</field>
    <field name="model_id" ref="ir.model_ir_attachment"/>
    <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="False"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_unlink" eval="False"/>
    <field name="domain_force">[
        '|',
        ('portal_user_ids', 'in', [user.partner_id.id]),
        ('directory_id.portal_user_ids', 'in', [user.partner_id.id])
    ]</field>
</record>
```

---

## 4. UI/UX 設計

### 4.1 Portal 頁面樣式

- 使用 Odoo Portal 標準 Bootstrap 樣式
- 卡片式目錄顯示（響應式 grid）
- 列表式檔案顯示
- 圖示區分檔案類型（PDF、圖片、文件等）

### 4.2 互動設計

| 動作 | 行為 |
|------|------|
| 點擊目錄卡片 | 進入目錄內容頁面 |
| 點擊「預覽」 | 在新分頁開啟預覽（支援的格式） |
| 點擊「下載」 | 直接下載檔案 |
| 點擊「下載全部」 | 下載目錄內所有檔案為 ZIP |
| 麵包屑導航 | 返回上層目錄或主頁面 |

### 4.3 空狀態處理

```html
<!-- 沒有分享的文件時 -->
<div class="text-center py-5">
    <i class="fa fa-folder-open-o fa-3x text-muted mb-3"></i>
    <h4>目前沒有分享給您的文件</h4>
    <p class="text-muted">當有人分享文件給您時，將會顯示在這裡。</p>
</div>
```

---

## 5. 實作計畫

### 5.1 Phase 1: 資料模型（預計 1 小時）
- [ ] 在 `document.directory` 新增 `portal_user_ids` 欄位
- [ ] 在 `ir.attachment` 新增 `portal_user_ids` 欄位
- [ ] 更新表單視圖顯示新欄位
- [ ] 新增 Security Rules

### 5.2 Phase 2: Portal Controller（預計 2 小時）
- [ ] 建立 `controllers/portal.py`
- [ ] 實作主頁面路由 `/my/documents`
- [ ] 實作目錄內容路由
- [ ] 實作檔案預覽/下載路由
- [ ] 實作目錄 ZIP 下載路由
- [ ] 實作權限檢查邏輯

### 5.3 Phase 3: Portal Templates（預計 2 小時）
- [ ] 建立 `views/portal_templates.xml`
- [ ] 設計主頁面模板
- [ ] 設計目錄內容模板
- [ ] 設計檔案預覽模板
- [ ] 新增 Portal 首頁計數器

### 5.4 Phase 4: 測試與優化（預計 1 小時）
- [ ] 測試權限繼承邏輯
- [ ] 測試各種檔案格式預覽
- [ ] 測試 ZIP 下載功能
- [ ] 效能優化（大量檔案時）

---

## 6. 測試案例

### 6.1 權限測試

| 測試案例 | 預期結果 |
|---------|---------|
| Portal User A 被加入目錄 X | A 可以在 Portal 看到目錄 X |
| Portal User A 存取目錄 X 的子目錄 | A 可以存取（繼承權限） |
| Portal User A 存取目錄 X 的檔案 | A 可以存取（繼承權限） |
| Portal User B 存取目錄 X | 403 禁止存取 |
| Portal User A 被加入檔案 Y（無目錄） | A 可以在「我的檔案」看到檔案 Y |
| 內部使用者存取 Portal 頁面 | 可以存取（有更高權限） |

### 6.2 功能測試

| 測試案例 | 預期結果 |
|---------|---------|
| 預覽 PDF 檔案 | 在瀏覽器開啟 PDF viewer |
| 預覽 PNG 圖片 | 直接顯示圖片 |
| 預覽 DOCX 檔案 | 顯示「不支援預覽」，提供下載 |
| 下載單一檔案 | 正確下載檔案 |
| 下載目錄為 ZIP | 下載包含所有檔案的 ZIP |
| 空目錄顯示 | 顯示「此目錄沒有檔案」訊息 |

---

## 7. 未來擴展（Out of Scope）

以下功能不在本次實作範圍，但可考慮未來版本：

- Portal 使用者上傳檔案到分享的目錄
- 檔案留言/評論功能
- 檔案版本歷史
- 檔案到期日設定
- 下載統計和追蹤
- 批量選擇下載

---

## Appendix: 相關參考

### Odoo Portal 開發文件
- [Portal Access](https://www.odoo.com/documentation/18.0/developer/reference/frontend/portal.html)
- [Website Controllers](https://www.odoo.com/documentation/18.0/developer/reference/frontend/controllers.html)

### 現有模組檔案
- `models/document_directory.py` - 目錄模型
- `models/ir_attachment.py` - 附件擴展
- `controllers/sh_download_directories.py` - 現有下載控制器
