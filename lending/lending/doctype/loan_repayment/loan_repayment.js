// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

lending.common.setup_filters("Loan Repayment");

frappe.ui.form.on('Loan Repayment', {
	setup(frm) {
		frm.ignore_doctypes_on_cancel_all = ["Process Loan Classification", "Loan Repayment Repost", "Loan Adjustment",
			"Loan Restructure", "Loan Repayment Schedule", "Sales Invoice", "Loan Demand", "Loan Interest Accrual"];
		if (frappe.meta.has_field("Loan Repayment", "repay_from_salary")) {
			frm.add_fetch("against_loan", "repay_from_salary", "repay_from_salary");
		}
	},

	onload: function(frm) {
		frm.set_query('against_loan', function() {
			return {
				'filters': {
					'docstatus': 1
				}
			};
		});

		frm.set_query('payment_account', function() {
			return {
				'filters': {
					"company": frm.doc.company,
					"is_group": 0
				}
			};
		});

		if (frm.doc.against_loan && frm.doc.value_date && frm.is_new()) {
			frm.trigger('calculate_repayment_amounts');
		}
	},

	refresh: function(frm) {
		// GL Preview/View buttons
		// Draft (docstatus=0): Preview button → shows GL entries that will be created
		// Submitted (docstatus=1): View button → opens actual GL entries in General Ledger
		if (!frm.is_new()) {
			if (frm.doc.docstatus == 0) {
				// Draft: Preview button
				frm.add_custom_button(__("Accounting Ledger"), function() {
					frappe.call({
						type: "GET",
						method: "lending.lending.doctype.loan_repayment.loan_repayment.show_accounting_ledger_preview",
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
				// Submitted: View button
				frm.add_custom_button(__("Accounting Ledger"), function() {
					frappe.route_options = {
						voucher_type: frm.doc.doctype,
						voucher_no: frm.doc.name
					};
					frappe.set_route("query-report", "General Ledger");
				}, __("View"));
			}
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
			id: col.fieldname,
			content: col.label,
			width: col.width || 150,
			format: col.fieldtype === "Currency" ? (value) => format_currency(value) : undefined,
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
	value_date : function(frm) {
		frm.trigger('calculate_repayment_amounts');
	},

	against_loan: function(frm) {
		if (frm.doc.value_date) {
			frm.trigger('calculate_repayment_amounts');
		}
	},
	against_loan: function(frm) {
		frm.set_query('loan_disbursement', function() {
			return {
				'filters': {
					'docstatus': 1,
					'against_loan': frm.doc.against_loan
				}
			};
		});

		frm.set_query('loan_adjustment', function() {
			return {
				'filters': {
					'docstatus': 1,
					'loan': frm.doc.against_loan,
				}
			};
		});
	},
	repayment_type: function(frm) {
		if (frm.doc.value_date) {
			frm.trigger('calculate_repayment_amounts');
		}
	},

	calculate_repayment_amounts: function(frm) {
		frappe.call({
			method: 'lending.lending.doctype.loan_repayment.loan_repayment.calculate_amounts',
			args: {
				'against_loan': frm.doc.against_loan,
				'posting_date': frm.doc.value_date,
				'payment_type': frm.doc.repayment_type
			},
			callback: function(r) {
				let amounts = r.message;
				frm.set_df_property('amount_paid', 'read_only', frm.doc.payment_type == "Loan Closure" ? 1:0);

				frm.set_value('pending_principal_amount', amounts['pending_principal_amount']);
				if (frm.doc.is_term_loan || frm.doc.payment_type == "Loan Closure") {
					frm.set_value('payable_principal_amount', amounts['payable_principal_amount']);

					if (!frm.doc.amount_paid) {
						frm.set_value('amount_paid', amounts['payable_amount']);
					}
				}
				frm.set_value('interest_payable', amounts['interest_amount']);
				frm.set_value('penalty_amount', amounts['penalty_amount']);
				frm.set_value('payable_amount', amounts['payable_amount']);
				frm.set_value('total_charges_payable', amounts['total_charges_payable']);

				if (amounts["charges"]) {
					frm.clear_table("pending_charges");
					amounts["charges"].forEach(d => {
						let row = frm.add_child('pending_charges');
						row.sales_invoice = d.sales_invoice;
						row.pending_charge_amount = d.pending_charge_amount;
					})
					frm.refresh_field('pending_charges');
				}

			}
		});
	}
});
