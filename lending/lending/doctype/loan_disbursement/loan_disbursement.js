// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

lending.common.setup_filters("Loan Disbursement");

frappe.ui.form.on('Loan Disbursement', {
	setup(frm) {
		frm.ignore_doctypes_on_cancel_all = ["Loan Security Deposit", "Loan Repayment Schedule",
			"Sales Invoice", "Loan Interest Accrual", "Loan Demand", "Loan Restructure", "Loan Repayment", "Process Loan Classification"];
	},
	refresh: function(frm) {
		// Preview button for GL Entries (same as Sales Invoice pattern)
		// Draft state: Preview → shows GL entries that will be created
		// Submitted state: View → shows actual GL entries
		if (!frm.is_new()) {
			if (frm.doc.docstatus == 0) {
				// Draft: Preview button
				frm.add_custom_button(__("Accounting Ledger"), function() {
					frappe.call({
						type: "GET",
						method: "lending.lending.doctype.loan_disbursement.loan_disbursement.show_accounting_ledger_preview",
						args: {
							company: frm.doc.company,
							doctype: frm.doc.doctype,
							docname: frm.doc.name,
						},
						callback: function(response) {
							if (response.message.gl_data.length === 0) {
								frappe.msgprint(__("<strong>No Impact on Accounting Ledger</strong>"));
							} else {
								frm.events.show_gl_preview_dialog(frm, response.message);
							}
						},
					});
				}, __("Preview"));
			} else if (frm.doc.docstatus == 1) {
				// Submitted: View button → opens actual GL entries
				frm.add_custom_button(__("Accounting Ledger"), function() {
					frappe.route_options = {
						voucher_type: frm.doc.doctype,
						voucher_no: frm.doc.name
					};
					frappe.set_route("query-report", "General Ledger");
				}, __("View"));
			}
		}

		frm.set_query('against_loan', function() {
			return {
				'filters': {
					'docstatus': 1,
					"status": ["in",["Sanctioned","Active", "Partially Disbursed"]],
				}
			}
		})
		if (frm.doc.docstatus == 1 && frm.doc.repayment_schedule_type && frm.doc.status != "Closed") {
			frm.add_custom_button(__('Loan Repayment'), function() {
				frm.trigger("make_repayment_entry");
			},__('Create'));
		}
	},
	show_gl_preview_dialog: function(frm, data) {
		let dialog = new frappe.ui.Dialog({
			size: "extra-large",
			title: __("Accounting Ledger Preview"),
			fields: [{
				fieldtype: "HTML",
				fieldname: "gl_preview_html",
			}],
		});

		// Format columns for frappe.DataTable
		// id = fieldname for data mapping, content = header text
		let columns = data.gl_columns.map(col => ({
			id: col.fieldname,  // Use fieldname as id to match data keys
			content: col.label,
			width: col.width,
			format: col.fieldtype === "Currency" ? (value) => format_currency(value) : undefined,
			options: col.options,  // For Dynamic Link
		}));

		// Build datatable
		let datatable_options = {
			columns: columns,
			data: data.gl_data,
			dynamicRowHeight: true,
			checkboxColumn: false,
			inlineFilters: true,
		};

		setTimeout(() => {
			new frappe.DataTable(dialog.get_field("gl_preview_html").wrapper, datatable_options);
		}, 200);

		dialog.show();
	},
	make_repayment_entry: function(frm) {
		frappe.call({
			args: {
				"loan": frm.doc.against_loan,
				"applicant_type": frm.doc.applicant_type,
				"applicant": frm.doc.applicant,
				"loan_product": frm.doc.loan_product,
				"company": frm.doc.company,
				"loan_disbursement": frm.doc.name,
				"as_dict": 1
			},
			method: "lending.lending.doctype.loan.loan.make_repayment_entry",
			callback: function (r) {
				if (r.message)
					var doc = frappe.model.sync(r.message)[0];
				frappe.set_route("Form", doc.doctype, doc.name);
			}
		})
	},
});
