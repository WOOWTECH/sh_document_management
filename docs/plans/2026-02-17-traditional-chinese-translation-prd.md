# Document Management Module - Traditional Chinese Translation PRD

# 文件管理模組 - 繁體中文翻譯 PRD

---

## Overview | 概述

This PRD defines the scope and implementation plan for adding Traditional Chinese (zh_TW) translation support to the `sh_document_management` Odoo 18 module.

本 PRD 定義為 `sh_document_management` Odoo 18 模組新增繁體中文 (zh_TW) 翻譯的範圍與實作計劃。

---

## Objectives | 目標

1. Create `i18n/zh_TW.po` translation file
2. Translate all user-facing strings including:
   - Menu items
   - Form labels and field names
   - Button text
   - Portal page content
   - Error messages
   - Help text and descriptions

---

## Translation Scope | 翻譯範圍

### 1. Menu Items | 選單項目

| English | 繁體中文 |
|---------|----------|
| Document Management | 文件管理 |
| Document Directory | 文件目錄 |
| Directory | 目錄 |
| Directories | 目錄 |
| Directory Tags | 目錄標籤 |
| Document Tags | 文件標籤 |

### 2. Form Fields | 表單欄位

| English | 繁體中文 |
|---------|----------|
| Directory Name | 目錄名稱 |
| Name | 名稱 |
| Parent Directory | 上層目錄 |
| Files | 檔案 |
| Sub Directories | 子目錄 |
| Directory Tags | 目錄標籤 |
| Document Tags | 文件標籤 |
| Users | 使用者 |
| Portal Users | Portal 使用者 |
| Visible Directory | 可見目錄 |
| Visible Directory Setting | 可見目錄設定 |
| Directory Details | 目錄詳情 |
| Share URL | 分享連結 |
| Access Token | 存取權杖 |

### 3. Buttons | 按鈕

| English | 繁體中文 |
|---------|----------|
| Share | 分享 |
| Download | 下載 |
| Download ZIP | 下載 ZIP |
| Download All as ZIP | 全部下載為 ZIP |
| Preview | 預覽 |
| Delete | 刪除 |
| Open | 開啟 |
| View Related Files | 檢視相關檔案 |
| Export as zip | 匯出為 ZIP |

### 4. Portal Page Content | Portal 頁面內容

| English | 繁體中文 |
|---------|----------|
| Documents | 文件 |
| View shared documents | 檢視共享文件 |
| My Documents | 我的文件 |
| My Directories | 我的目錄 |
| My Files | 我的檔案 |
| files | 個檔案 |
| Sub-directories | 子目錄 |
| No directories shared with you | 沒有與您共享的目錄 |
| No files directly shared with you | 沒有直接與您共享的檔案 |
| No documents shared with you yet | 尚無文件與您共享 |
| When someone shares documents with you, they will appear here. | 當有人與您共享文件時，將會顯示在這裡。 |
| This directory is empty | 此目錄是空的 |

### 5. Table Headers | 表格標題

| English | 繁體中文 |
|---------|----------|
| Name | 名稱 |
| Type | 類型 |
| Size | 大小 |
| Date | 日期 |
| Actions | 操作 |
| Created By | 建立者 |
| Create Date | 建立日期 |

### 6. Filters & Groups | 篩選與群組

| English | 繁體中文 |
|---------|----------|
| Visible Directory | 可見目錄 |
| My Directory | 我的目錄 |
| Group By | 群組依據 |
| Created By | 建立者 |
| Parent Directory | 上層目錄 |
| Create Date | 建立日期 |

### 7. Model Descriptions | 模型描述

| English | 繁體中文 |
|---------|----------|
| Document Directory | 文件目錄 |
| Directory Tags | 目錄標籤 |
| Document Tags | 文件標籤 |

---

## Implementation | 實作方式

### File Structure | 檔案結構

```
sh_document_management/
├── i18n/
│   └── zh_TW.po          # Traditional Chinese translation
├── __manifest__.py       # No changes needed (Odoo auto-loads i18n)
└── ...
```

### PO File Format | PO 檔案格式

```po
# Translation of Odoo Server.
# This file contains the translation of the following modules:
# * sh_document_management
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server 18.0\n"
"Language: zh_TW\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#. module: sh_document_management
#: model:ir.model,name:sh_document_management.model_document_directory
msgid "Document Directory"
msgstr "文件目錄"
```

---

## Testing | 測試

1. Install/upgrade the module
2. Go to Settings → Translations → Languages
3. Ensure Traditional Chinese is installed
4. Change user language to Traditional Chinese
5. Verify all strings are translated in:
   - Backend views (forms, lists, kanban)
   - Portal pages
   - Menu items
   - Buttons and actions

---

## Success Criteria | 成功標準

- [ ] All menu items display in Traditional Chinese
- [ ] All form labels and field names are translated
- [ ] All buttons show Chinese text
- [ ] Portal pages fully translated
- [ ] No missing translations (no English text when Chinese is selected)

---

## Version | 版本

- Module Version: 0.4.0
- Date: 2026-02-17
- Author: Claude Code AI Assistant
