/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { SHDocumentKanbanRecord } from "@sh_document_management/views/sh_documents_kanban/document_management_kanban_record";
export class SHDocumentKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
    }
}

SHDocumentKanbanRenderer.components = {
    ...KanbanRenderer.components,
    KanbanRecord: SHDocumentKanbanRecord,
};
