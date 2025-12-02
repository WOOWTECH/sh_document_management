/** @odoo-module **/

import { registry } from "@web/core/registry";

import { kanbanView } from "@web/views/kanban/kanban_view";
import { SHDocumentKanbanRenderer } from "@sh_document_management/views/sh_documents_kanban/document_management_kanban_renderer";

export const SHDocumentKanbanView = {
    ...kanbanView,
    Renderer: SHDocumentKanbanRenderer,
};

registry.category("views").add("sh_documents_kanban", SHDocumentKanbanView);
