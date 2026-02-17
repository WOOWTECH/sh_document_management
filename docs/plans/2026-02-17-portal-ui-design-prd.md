# PRD: Portal Document UI Redesign

## Document Information
- **Module**: sh_document_management
- **Feature**: Portal UI Redesign
- **Version**: 0.3.1
- **Date**: 2026-02-17
- **Status**: Design

---

## 1. Design Direction

### 1.1 Aesthetic: Minimal & Clean
Inspired by **Notion**, **Linear**, and **Dropbox Paper** - focused on content, generous whitespace, refined typography, and subtle interactions.

### 1.2 Key Principles
- **Content-first**: Documents are the hero, not decorations
- **Subtle hierarchy**: Use spacing and typography weight instead of borders/colors
- **Refined details**: Small icons (16-20px), thin strokes, precise spacing
- **Calm palette**: Neutral grays with single accent color
- **Purposeful motion**: Subtle hover states, no gratuitous animation

### 1.3 Problems with Current Design
- Icons too large (fa-2x, fa-3x) - overwhelming
- Heavy card shadows - feels dated
- Dense layout - needs breathing room
- Generic Bootstrap styling - lacks character

---

## 2. Visual Specifications

### 2.1 Typography
```css
/* Primary: System font stack for crisp rendering */
--font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Headings: Lighter weight, larger sizes */
--heading-xl: 600 28px/1.2 var(--font-primary);
--heading-lg: 600 20px/1.3 var(--font-primary);
--heading-md: 500 16px/1.4 var(--font-primary);
--heading-sm: 500 14px/1.4 var(--font-primary);

/* Body */
--text-base: 400 14px/1.6 var(--font-primary);
--text-sm: 400 13px/1.5 var(--font-primary);
--text-xs: 400 12px/1.5 var(--font-primary);
```

### 2.2 Color Palette
```css
/* Neutrals - Cool gray scale */
--color-bg: #FAFAFA;
--color-surface: #FFFFFF;
--color-border: #E5E5E5;
--color-border-subtle: #F0F0F0;

/* Text */
--color-text-primary: #1A1A1A;
--color-text-secondary: #6B6B6B;
--color-text-tertiary: #9B9B9B;

/* Accent - Subtle blue */
--color-accent: #2563EB;
--color-accent-hover: #1D4ED8;
--color-accent-subtle: #EFF6FF;

/* States */
--color-hover: #F5F5F5;
--color-active: #EBEBEB;
```

### 2.3 Spacing System
```css
/* 4px base unit */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
```

### 2.4 Icons
- **Size**: 16px (small), 20px (medium) - NEVER larger
- **Style**: Line icons, 1.5px stroke
- **Color**: `--color-text-secondary` default, `--color-text-primary` on hover

---

## 3. Component Specifications

### 3.1 Page Header
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Documents                                              │
│  ─────────────────────────────────────────             │
│  View and download your shared files                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
- Title: 28px, font-weight 600
- Subtitle: 14px, color-text-secondary
- Bottom border: 1px solid --color-border-subtle
- Padding: 32px 0

### 3.2 Section Header
```
Directories                                          3 items
```
- Label: 12px uppercase, letter-spacing 0.5px, color-text-tertiary
- Count: 12px, color-text-tertiary
- Margin-bottom: 16px

### 3.3 Directory Card (Compact)
```
┌─────────────────────────────────────────┐
│ 📁  Project Documents                   │
│     5 files · Updated 2 days ago        │
└─────────────────────────────────────────┘
```
- Background: white
- Border: 1px solid --color-border
- Border-radius: 8px
- Padding: 16px
- Icon: 16px, inline with text
- Hover: background --color-hover, border-color --color-border

### 3.4 File Row (List Style)
```
┌─────────────────────────────────────────────────────────┐
│ 📄  Proposal_v2.pdf          PDF    2.4 MB    Feb 15    │
│                                              ⬇️  👁️     │
└─────────────────────────────────────────────────────────┘
```
- Single row layout
- Icon: 16px
- Name: font-weight 500
- Metadata: color-text-tertiary, separated by middot (·)
- Actions: appear on hover, right-aligned
- Hover: background --color-hover

### 3.5 Breadcrumb
```
Documents  /  Project Files  /  Design Assets
```
- Font-size: 13px
- Separator: " / " in color-text-tertiary
- Current page: color-text-primary, no link
- Links: color-text-secondary, hover underline

### 3.6 Action Buttons
```css
/* Primary - Download All */
.btn-primary {
  background: var(--color-accent);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

/* Secondary - Individual actions */
.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  background: transparent;
}
.btn-icon:hover {
  background: var(--color-hover);
  color: var(--color-text-primary);
}
```

---

## 4. Page Layouts

### 4.1 Main Page (`/my/documents`)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Documents                                              │
│  View and download your shared files                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  DIRECTORIES                                    3 items │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │ 📁 Project   │ │ 📁 Contracts │ │ 📁 Reports   │    │
│  │ 5 files      │ │ 3 files      │ │ 8 files      │    │
│  └──────────────┘ └──────────────┘ └──────────────┘    │
│                                                         │
│  FILES                                          2 items │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📄 NDA_signed.pdf       PDF · 245 KB · Feb 10   │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ 📊 Q4_Report.xlsx      XLSX · 1.2 MB · Feb 8    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Directory Page (`/my/documents/directory/<id>`)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Documents / Project Files                              │
│                                                         │
│  Project Files                        [Download All ↓]  │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  SUBDIRECTORIES                                 1 item  │
│                                                         │
│  ┌──────────────┐                                      │
│  │ 📁 Designs   │                                      │
│  │ 3 files      │                                      │
│  └──────────────┘                                      │
│                                                         │
│  FILES                                          5 items │
│                                                         │
│  Name                    Type     Size      Date       │
│  ─────────────────────────────────────────────────────  │
│  📄 Requirements.pdf     PDF      456 KB    Feb 15     │
│  📄 Wireframes.pdf       PDF      2.1 MB    Feb 14     │
│  🖼️ Logo.png             PNG      124 KB    Feb 12     │
│  📊 Budget.xlsx          XLSX     89 KB     Feb 10     │
│  📝 Notes.txt            TXT      12 KB     Feb 8      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Empty States

### 5.1 No Documents
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                        📁                               │
│                                                         │
│              No documents shared yet                    │
│                                                         │
│     When someone shares files with you,                 │
│     they'll appear here.                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
- Icon: 32px, color-text-tertiary
- Title: 16px, font-weight 500
- Description: 14px, color-text-secondary
- Centered, generous padding

### 5.2 Empty Directory
```
This directory is empty
```
- Simple inline text, color-text-tertiary
- No large icons or boxes

---

## 6. Interaction States

### 6.1 Hover States
- **Directory card**: subtle background shift, border darkens
- **File row**: background highlight, actions become visible
- **Links**: underline appears
- **Buttons**: slight darken

### 6.2 Loading State
- Simple skeleton lines (no spinners)
- Pulse animation on content areas

### 6.3 Action Feedback
- Download: button shows checkmark briefly
- No toast notifications for simple actions

---

## 7. Implementation Notes

### 7.1 CSS Structure
```
static/src/css/
└── portal_documents.css    # Custom portal styles
```

### 7.2 Asset Registration
```python
'assets': {
    'web.assets_frontend': [
        'sh_document_management/static/src/css/portal_documents.css',
    ],
}
```

### 7.3 Template Updates
- Simplify HTML structure
- Remove excessive Bootstrap classes
- Use semantic HTML (article, section, nav)
- Add custom CSS classes for styling

---

## 8. File Type Icons

| Type | Icon | Color |
|------|------|-------|
| PDF | `fa-file-pdf-o` | #DC2626 (red-600) |
| Image | `fa-file-image-o` | #2563EB (blue-600) |
| Word | `fa-file-word-o` | #2563EB (blue-600) |
| Excel | `fa-file-excel-o` | #16A34A (green-600) |
| PowerPoint | `fa-file-powerpoint-o` | #EA580C (orange-600) |
| Text | `fa-file-text-o` | #6B7280 (gray-500) |
| Archive | `fa-file-archive-o` | #CA8A04 (yellow-600) |
| Other | `fa-file-o` | #9CA3AF (gray-400) |

---

## 9. Responsive Behavior

### Desktop (>1024px)
- 3-column grid for directories
- Full table for files

### Tablet (768-1024px)
- 2-column grid for directories
- Simplified table (hide some columns)

### Mobile (<768px)
- Single column
- Stack file metadata vertically
- Larger touch targets (48px min)
