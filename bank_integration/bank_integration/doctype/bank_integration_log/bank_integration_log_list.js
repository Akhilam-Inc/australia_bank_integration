frappe.listview_settings['Bank Integration Log'] = {
    add_fields: ["status", "status_code", "method", "url"],
    get_indicator: function(doc) {
        if (doc.status) {
            const status = doc.status.toLowerCase();

            if (status === 'error' || status === 'failed' || status === 'failure') {
                return [__(doc.status), "red", "status,=," + doc.status];
            } else if (status === 'success' || status === 'completed' || status === 'ok') {
                return [__(doc.status), "green", "status,=," + doc.status];
            } else if (status === 'warning' || status === 'warn') {
                return [__(doc.status), "orange", "status,=," + doc.status];
            } else if (status === 'info' || status === 'information' || status === 'processing') {
                return [__(doc.status), "blue", "status,=," + doc.status];
            } else {
                return [__(doc.status), "gray", "status,=," + doc.status];
            }
        }
        return ["Unknown", "gray"];
    },

    formatters: {
        status_code: function(value) {
            if (value) {
                const code = parseInt(value);
                if (code >= 200 && code < 300) {
                    return `<span class="text-success">${value}</span>`;
                } else if (code >= 400 && code < 500) {
                    return `<span class="text-warning">${value}</span>`;
                } else if (code >= 500) {
                    return `<span class="text-danger">${value}</span>`;
                }
            }
            return value;
        },

        method: function(value) {
            if (value) {
                return `<code class="text-muted">${value}</code>`;
            }
            return value;
        }
    },

    onload: function(listview) {
        listview.page.add_menu_item(__("Clear All Logs"), function() {
            frappe.confirm(
                __("Are you sure you want to delete all Bank Integration Logs?"),
                function() {
                    frappe.call({
                        method: "frappe.desk.bulk_update.submit_cancel_or_update_docs",
                        args: {
                            doctype: "Bank Integration Log",
                            action: "delete",
                            docnames: listview.get_checked_items(true)
                        },
                        callback: function() {
                            listview.refresh();
                        }
                    });
                }
            );
        });
    }
};
