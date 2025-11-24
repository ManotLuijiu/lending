import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

LOAN_CUSTOM_FIELDS = {
    "Sales Invoice": [
        {
            "fieldname": "loan",
            "label": "Loan",
            "fieldtype": "Link",
            "options": "Loan",
            "insert_after": "customer",
            "print_hide": 1,
        },
        {
            "fieldname": "loan_disbursement",
            "label": "Loan Disbursement",
            "fieldtype": "Link",
            "options": "Loan Disbursement",
            "insert_after": "loan",
            "read_only": 1,
            "print_hide": 1,
        },
        {
            "fieldname": "loan_repayment",
            "label": "Loan Repayment",
            "fieldtype": "Link",
            "options": "Loan Repayment",
            "insert_after": "loan_disbursement",
            "read_only": 1,
            "print_hide": 1,
        },
        {
            "fieldname": "value_date",
            "fieldtype": "Date",
            "label": "Value Date",
            "insert_after": "posting_date",
            "search_index": 1,
        },
    ],
    "Company": [
        {
            "fieldname": "loan_tab",
            "fieldtype": "Tab Break",
            "label": "Loan",
            "insert_after": "hr_and_payroll_tab",
        },
        {
            "fieldname": "loan_settings",
            "label": "Loan Settings",
            "fieldtype": "Section Break",
            "insert_after": "loan_tab",
        },
        {
            "fieldname": "loan_restructure_limit",
            "label": "Restructure Limit % (Overall)",
            "fieldtype": "Percent",
            "insert_after": "loan_settings",
        },
        {
            "fieldname": "watch_period_post_loan_restructure_in_days",
            "label": "Watch Period Post Loan Restructure (In Days)",
            "fieldtype": "Int",
            "insert_after": "loan_restructure_limit",
        },
        {
            "fieldname": "interest_day_count_convention",
            "label": "Interest Day-Count Convention",
            "fieldtype": "Select",
            "options": "Actual/365\nActual/Actual\n30/365\n30/360\nActual/360",
            "insert_after": "watch_period_post_loan_restructure_in_days",
        },
        {
            "fieldname": "min_days_bw_disbursement_first_repayment",
            "label": "Minimum days between Disbursement date and first Repayment date",
            "fieldtype": "Int",
            "insert_after": "interest_day_count_convention",
            "non_negative": 1,
        },
        {
            "fieldname": "loan_accrual_frequency",
            "label": "Loan Accrual Frequency",
            "fieldtype": "Select",
            "options": "Daily\nWeekly\nMonthly",
            "insert_after": "min_days_bw_disbursement_first_repayment",
        },
        {
            "fieldname": "loan_column_break",
            "fieldtype": "Column Break",
            "insert_after": "min_days_bw_disbursement_first_repayment",
        },
        {
            "fieldname": "collection_offset_logic_based_on",
            "label": "Collection Offset Logic Based On",
            "fieldtype": "Select",
            "options": "NPA Flag\nDays Past Due",
            "insert_after": "loan_column_break",
        },
        {
            "fieldname": "days_past_due_threshold",
            "label": "Days Past Due Threshold",
            "fieldtype": "Int",
            "insert_after": "collection_offset_logic_based_on",
            "non_negative": 1,
        },
        {
            "fieldname": "days_past_due_threshold_for_auto_write_off",
            "label": "Days Past Due Threshold For Auto Write Off",
            "fieldtype": "Int",
            "insert_after": "days_past_due_threshold",
            "non_negative": 1,
        },
        {
            "fieldname": "collection_offset_sequence_for_sub_standard_asset",
            "label": "Collection Offset Sequence for Sub Standard Asset",
            "fieldtype": "Link",
            "options": "Loan Demand Offset Order",
            "insert_after": "days_past_due_threshold",
        },
        {
            "fieldname": "collection_offset_sequence_for_standard_asset",
            "label": "Collection Offset Sequence for Standard Asset",
            "fieldtype": "Link",
            "options": "Loan Demand Offset Order",
            "insert_after": "collection_offset_sequence_for_sub_standard_asset",
        },
        {
            "fieldname": "collection_offset_sequence_for_written_off_asset",
            "label": "Collection Offset Sequence for Written Off Asset",
            "fieldtype": "Link",
            "options": "Loan Demand Offset Order",
            "insert_after": "collection_offset_sequence_for_standard_asset",
        },
        {
            "fieldname": "collection_offset_sequence_for_settlement_collection",
            "label": "Collection Offset Sequence for Settlement Collection",
            "fieldtype": "Link",
            "options": "Loan Demand Offset Order",
            "insert_after": "collection_offset_sequence_for_written_off_asset",
        },
        {
            "fieldname": "loan_section_break_2",
            "fieldtype": "Section Break",
            "insert_after": "collection_offset_sequence_for_settlement_collection",
        },
        {
            "fieldname": "loan_classification_ranges",
            "label": "Loan Classification Ranges",
            "fieldtype": "Table",
            "options": "Loan Classification Range",
            "insert_after": "loan_section_break_2",
        },
        {
            "fieldname": "irac_provisioning_configuration",
            "label": "IRAC Provisioning Configuration",
            "fieldtype": "Table",
            "options": "Loan IRAC Provisioning Configuration",
            "insert_after": "loan_classification_ranges",
        },
    ],
    "Customer": [
        {
            "fieldname": "loan_details_tab",
            "label": "Loan Details",
            "fieldtype": "Tab Break",
            "insert_after": "email_id",
        },
        {
            "fieldname": "loan_details_section",
            "fieldtype": "Section Break",
            "label": "Applicant",
            "insert_after": "loan_details_tab",
        },
        {
            "fieldname": "loan_details_column_left",
            "fieldtype": "Column Break",
            "insert_after": "loan_details_section",
        },
        {
            "fieldname": "is_npa",
            "label": "Is NPA",
            "fieldtype": "Check",
            "insert_after": "loan_details_column_left",
        },
        {
            "fieldname": "ld_custom_first_created",
            "label": "First Created",
            "fieldtype": "Link",
            "options": "Vehicle Loan Application",
            "insert_after": "is_npa",
        },
        {
            "fieldname": "ld_custom_id_card_number",
            "label": "ID Card Number",
            "fieldtype": "Data",
            "insert_after": "ld_custom_first_created",
            "description": "ID Card Number for the customer",
        },
        {
            "fieldname": "ld_custom_house_number",
            "label": "House Number",
            "fieldtype": "Data",
            "insert_after": "ld_custom_id_card_number",
        },
        {
            "fieldname": "ld_custom_village",
            "label": "Village",
            "fieldtype": "Data",
            "insert_after": "ld_custom_house_number",
        },
        {
            "fieldname": "ld_custom_moo",
            "label": "Moo",
            "fieldtype": "Data",
            "insert_after": "ld_custom_village",
        },
        {
            "fieldname": "ld_custom_soi",
            "label": "Soi",
            "fieldtype": "Data",
            "insert_after": "ld_custom_moo",
        },
        {
            "fieldname": "ld_custom_road",
            "label": "Road",
            "fieldtype": "Data",
            "insert_after": "ld_custom_soi",
        },
        {
            "fieldname": "loan_details_column_right",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_road",
        },
        {
            "fieldname": "ld_custom_contact_subdistrict",
            "label": "Subdistrict",
            "fieldtype": "Data",
            "insert_after": "loan_details_column_right",
        },
        {
            "fieldname": "ld_custom_contact_district",
            "label": "District",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_subdistrict",
        },
        {
            "fieldname": "ld_custom_contact_province",
            "label": "Province",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_district",
        },
        {
            "fieldname": "ld_custom_contact_postal",
            "label": "Postal Code",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_province",
        },
        {
            "fieldname": "ld_custom_contact_fax",
            "label": "Fax",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_postal",
        },
        # Current Address
        {
            "fieldname": "ld_custom_current_address",
            "fieldtype": "Section Break",
            "label": "Current Address",
            "insert_after": "ld_custom_contact_fax",
            "collapsible": 1,
        },
        {
            "fieldname": "ld_custom_current_address_column_left",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_current_address",
        },
        {
            "fieldname": "ld_custom_same_as_id",
            "label": "Same As ID Address",
            "fieldtype": "Check",
            "insert_after": "ld_custom_current_address_column_left",
        },
        {
            "fieldname": "ld_custom_current_house_number",
            "label": "House Number",
            "fieldtype": "Data",
            "insert_after": "ld_custom_same_as_id",
        },
        {
            "fieldname": "ld_custom_current_village",
            "label": "Village",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_house_number",
        },
        {
            "fieldname": "ld_custom_current_moo",
            "label": "Moo",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_village",
        },
        {
            "fieldname": "ld_custom_current_soi",
            "label": "Soi",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_moo",
        },
        {
            "fieldname": "ld_custom_current_road",
            "label": "Road",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_soi",
        },
        {
            "fieldname": "ld_custom_current_subdistrict",
            "label": "Subdistrict",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_road",
        },
        {
            "fieldname": "ld_custom_current_address_column_right",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_current_subdistrict",
        },
        {
            "fieldname": "ld_custom_current_contact_district",
            "label": "District",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_address_column_right",
        },
        {
            "fieldname": "ld_custom_current_contact_province",
            "label": "Province",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_contact_district",
        },
        {
            "fieldname": "ld_custom_current_contact_postal",
            "label": "Postal Code",
            "fieldtype": "Data",
            "insert_after": "ld_custom_current_contact_province",
        },
        # Mailing Address
        {
            "fieldname": "ld_custom_mailing_address",
            "fieldtype": "Section Break",
            "label": "Mailing Address",
            "insert_after": "ld_custom_current_contact_postal",
            "collapsible": 1,
        },
        {
            "fieldname": "ld_custom_mailing_address_column_left",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_mailing_address",
        },
        {
            "fieldname": "ld_custom_mailing_same_as_id",
            "label": "Same As ID Address",
            "fieldtype": "Check",
            "insert_after": "ld_custom_mailing_address_column_left",
        },
        {
            "fieldname": "ld_custom_mailing_house_number",
            "label": "House Number",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_same_as_id",
        },
        {
            "fieldname": "ld_custom_mailing_village",
            "label": "Village",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_house_number",
        },
        {
            "fieldname": "ld_custom_mailing_moo",
            "label": "Moo",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_village",
        },
        {
            "fieldname": "ld_custom_mailing_soi",
            "label": "Soi",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_moo",
        },
        {
            "fieldname": "ld_custom_mailing_road",
            "label": "Road",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_soi",
        },
        {
            "fieldname": "ld_custom_mailing_subdistrict",
            "label": "Subdistrict",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_road",
        },
        {
            "fieldname": "ld_custom_mailing_address_column_right",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_mailing_subdistrict",
        },
        {
            "fieldname": "ld_custom_mailing_contact_district",
            "label": "District",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_address_column_right",
        },
        {
            "fieldname": "ld_custom_mailing_contact_province",
            "label": "Province",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_contact_district",
        },
        {
            "fieldname": "ld_custom_mailing_contact_postal",
            "label": "Postal Code",
            "fieldtype": "Data",
            "insert_after": "ld_custom_mailing_contact_province",
        },
        # Work Address
        {
            "fieldname": "ld_custom_work_address",
            "fieldtype": "Section Break",
            "label": "Work Address",
            "insert_after": "ld_custom_mailing_contact_postal",
            "collapsible": 1,
        },
        {
            "fieldname": "ld_custom_work_address_column_left",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_work_address",
        },
        {
            "fieldname": "ld_custom_work_house_number",
            "label": "House Number",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_address_column_left",
        },
        {
            "fieldname": "ld_custom_work_village",
            "label": "Village",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_house_number",
        },
        {
            "fieldname": "ld_custom_work_moo",
            "label": "Moo",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_village",
        },
        {
            "fieldname": "ld_custom_work_soi",
            "label": "Soi",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_moo",
        },
        {
            "fieldname": "ld_custom_work_road",
            "label": "Road",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_soi",
        },
        {
            "fieldname": "ld_custom_work_subdistrict",
            "label": "Subdistrict",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_road",
        },
        {
            "fieldname": "ld_custom_work_address_column_right",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_work_subdistrict",
        },
        {
            "fieldname": "ld_custom_work_contact_district",
            "label": "District",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_address_column_right",
        },
        {
            "fieldname": "ld_custom_work_contact_province",
            "label": "Province",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_contact_district",
        },
        {
            "fieldname": "ld_custom_work_contact_postal",
            "label": "Postal Code",
            "fieldtype": "Data",
            "insert_after": "ld_custom_work_contact_province",
        },
        # Contact Information
        {
            "fieldname": "ld_custom_contact_info",
            "fieldtype": "Section Break",
            "label": "Contact Information",
            "insert_after": "ld_custom_work_contact_postal",
            "collapsible": 1,
        },
        {
            "fieldname": "ld_custom_contact_info_column_left",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_contact_info",
        },
        {
            "fieldname": "ld_custom_phone",
            "label": "Phone",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_info_column_left",
        },
        {
            "fieldname": "ld_custom_mobile",
            "label": "Mobile",
            "fieldtype": "Data",
            "insert_after": "ld_custom_phone",
        },
        {
            "fieldname": "ld_custom_contact_info_column_right",
            "fieldtype": "Column Break",
            "insert_after": "ld_custom_mobile",
        },
        {
            "fieldname": "ld_custom_email",
            "label": "Email",
            "fieldtype": "Data",
            "insert_after": "ld_custom_contact_info_column_right",
        },
        {
            "fieldname": "ld_custom_line_id",
            "label": "Line ID",
            "fieldtype": "Data",
            "insert_after": "ld_custom_email",
        },
        {
            "fieldname": "ld_custom_social",
            "label": "Social",
            "fieldtype": "Data",
            "insert_after": "ld_custom_line_id",
        },
        {
            "fieldname": "ld_custom_google_map",
            "label": "Google Map",
            "fieldtype": "Data",
            "insert_after": "ld_custom_social",
        },
        {
            "fieldname": "ld_custom_work_place_google_map",
            "label": "Work Place Google Map",
            "fieldtype": "Data",
            "insert_after": "ld_custom_google_map",
        },
    ],
    "Item Default": [
        {
            "fieldname": "loan_defaults_section",
            "fieldtype": "Section Break",
            "label": "Loan Defaults",
            "insert_after": "deferred_revenue_account",
        },
        {
            "fieldname": "default_receivable_account",
            "fieldtype": "Link",
            "label": "Default Receivable Account",
            "options": "Account",
            "insert_after": "loan_defaults_section",
        },
        {
            "fieldname": "default_waiver_account",
            "fieldtype": "Link",
            "label": "Default Waiver Account",
            "options": "Account",
            "insert_after": "default_receivable_account",
        },
        {
            "fieldname": "column_break_yajs",
            "fieldtype": "Column Break",
            "insert_after": "default_waiver_account",
        },
        {
            "fieldname": "default_write_off_account",
            "fieldtype": "Link",
            "label": "Default Write Off Account",
            "options": "Account",
            "insert_after": "column_break_yajs",
        },
        {
            "fieldname": "default_suspense_account",
            "fieldtype": "Link",
            "label": "Default Suspense Account",
            "options": "Account",
            "insert_after": "default_write_off_account",
        },
    ],
    "Journal Entry": [
        {
            "fieldname": "loan_transfer",
            "fieldtype": "Link",
            "label": "Loan Transfer",
            "insert_after": "naming_series",
            "options": "Loan Transfer",
            "search_index": 1,
        },
        {
            "fieldname": "loan",
            "fieldtype": "Link",
            "label": "Loan",
            "insert_after": "loan_transfer",
            "options": "Loan",
            "search_index": 1,
        },
        {
            "fieldname": "value_date",
            "fieldtype": "Date",
            "label": "Value Date",
            "insert_after": "posting_date",
            "search_index": 1,
        },
    ],
    "GL Entry": [
        {
            "fieldname": "value_date",
            "fieldtype": "Date",
            "label": "Value Date",
            "insert_after": "posting_date",
            "search_index": 1,
        },
    ],
}


def fix_column_break_32_position():
    """
    Fix column_break_32 position by ensuring it has proper insert_after property.
    This addresses the issue where column_break_32 appears in loan_tab instead of stock_tab.
    """
    property_setter = frappe.db.get_value(
        "Property Setter",
        filters={
            "doc_type": "Company",
            "field_name": "column_break_32",
            "property": "insert_after",
        },
    )

    if property_setter:
        property_setter_doc = frappe.get_doc("Property Setter", property_setter)

        if property_setter_doc.value != "default_in_transit_warehouse":
            property_setter_doc.value = "default_in_transit_warehouse"
            property_setter_doc.save()
    else:
        make_property_setter(
            "Company",
            "column_break_32",
            "insert_after",
            "default_in_transit_warehouse",
            "Data",
            validate_fields_for_doctype=False,
        )


def make_property_setter_for_journal_entry():
    property_setter = frappe.db.get_value(
        "Property Setter",
        filters={
            "doc_type": "Journal Entry Account",
            "field_name": "reference_type",
            "property": "options",
        },
    )

    if property_setter:
        property_setter_doc = frappe.get_doc("Property Setter", property_setter)

        if "Loan Interest Accrual" not in property_setter_doc.value.split("\n"):
            property_setter_doc.value += "\n" + "Loan Interest Accrual"
            property_setter_doc.save()
    else:
        options = frappe.get_meta("Journal Entry Account").get_field("reference_type").options
        options += "\n" + "Loan Interest Accrual"

        make_property_setter(
            "Journal Entry Account",
            "reference_type",
            "options",
            options,
            "Text",
            validate_fields_for_doctype=False,
        )


def after_install():
    create_custom_fields(LOAN_CUSTOM_FIELDS, ignore_validate=True)
    make_property_setter_for_journal_entry()
    fix_column_break_32_position()


@frappe.whitelist()
def check_custom_fields():
    """
    Verify that all Lending app custom fields are properly installed.
    Can be called via bench console or as API endpoint.

    Returns:
        dict: Summary with status, total count, missing fields list
    """
    try:
        frappe.logger().info("Checking Lending app custom fields installation...")
        missing_fields = []
        total_fields = 0

        for doctypes, fields in LOAN_CUSTOM_FIELDS.items():
            if isinstance(fields, dict):
                # Only one field
                fields = [fields]

            if isinstance(doctypes, str):
                # Only one doctype
                doctypes = (doctypes,)

            for doctype in doctypes:
                for field in fields:
                    total_fields += 1
                    fieldname = field["fieldname"]

                    if not frappe.db.exists(
                        "Custom Field", {"dt": doctype, "fieldname": fieldname}
                    ):
                        missing_fields.append(
                            {
                                "doctype": doctype,
                                "fieldname": fieldname,
                                "label": field.get("label", fieldname),
                            }
                        )

        if missing_fields:
            frappe.logger().warning(
                f"Missing {len(missing_fields)} custom field(s) out of {total_fields}"
            )
            for field in missing_fields:
                frappe.logger().warning(
                    f"  - {field['doctype']}.{field['fieldname']} ({field['label']})"
                )

            return {
                "status": "incomplete",
                "total_fields": total_fields,
                "installed_fields": total_fields - len(missing_fields),
                "missing_fields": missing_fields,
                "message": f"Missing {len(missing_fields)} field(s)",
            }
        else:
            frappe.logger().info(f"✓ All {total_fields} Lending app custom fields are installed!")
            return {
                "status": "complete",
                "total_fields": total_fields,
                "installed_fields": total_fields,
                "missing_fields": [],
                "message": "All fields installed successfully",
            }

    except Exception as e:
        frappe.logger().error(f"Error checking Lending app custom fields: {str(e)}")
        return {"status": "error", "message": str(e), "missing_fields": []}


def before_uninstall():
    """Clean up custom fields and property setters before uninstalling lending app"""
    try:
        frappe.logger().info("Running Lending app pre-uninstallation cleanup...")

        # Remove custom fields
        delete_custom_fields(LOAN_CUSTOM_FIELDS)

        # Clean up property setters
        cleanup_property_setters()

        frappe.logger().info("Lending app pre-uninstallation cleanup completed successfully")
    except Exception as e:
        frappe.logger().error(f"Error during Lending app pre-uninstallation cleanup: {e}")
        # Don't raise - allow uninstall to continue even if cleanup fails


def delete_custom_fields(custom_fields):
    """
    Delete custom fields for lending app
    :param custom_fields: a dict like `{'Customer': [{fieldname: 'test', ...}]}`
    """
    deleted_count = 0

    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            # only one field
            fields = [fields]

        if isinstance(doctypes, str):
            # only one doctype
            doctypes = (doctypes,)

        for doctype in doctypes:
            fieldnames = [field["fieldname"] for field in fields]

            # Delete custom fields (bulk delete for efficiency)
            try:
                frappe.db.delete(
                    "Custom Field",
                    {
                        "fieldname": ("in", fieldnames),
                        "dt": doctype,
                    },
                )

                deleted_count += len(fieldnames)
                frappe.logger().info(f"Removed {len(fieldnames)} custom fields from {doctype}")

            except Exception as e:
                frappe.logger().error(f"Error deleting custom fields from {doctype}: {str(e)}")

            finally:
                frappe.clear_cache(doctype=doctype)

    # Commit the changes
    frappe.db.commit()
    frappe.logger().info(f"Total custom fields deleted: {deleted_count}")


def cleanup_property_setters():
    """Clean up property setters created by lending app"""
    try:
        # Clean up Journal Entry Account reference_type property setter
        # Remove "Loan Interest Accrual" from the options
        property_setter = frappe.db.get_value(
            "Property Setter",
            filters={
                "doc_type": "Journal Entry Account",
                "field_name": "reference_type",
                "property": "options",
            },
        )

        if property_setter:
            property_setter_doc = frappe.get_doc("Property Setter", property_setter)

            if "Loan Interest Accrual" in property_setter_doc.value:
                # Remove "Loan Interest Accrual" from options
                options_list = property_setter_doc.value.split("\n")
                options_list = [opt for opt in options_list if opt != "Loan Interest Accrual"]
                property_setter_doc.value = "\n".join(options_list)
                property_setter_doc.save()
                frappe.logger().info(
                    "Removed 'Loan Interest Accrual' from Journal Entry Account reference_type options"
                )

        # Note: We intentionally do NOT revert fix_column_break_32_position()
        # as it fixes a core ERPNext bug and reverting it could break other apps

        frappe.db.commit()

    except Exception as e:
        frappe.logger().error(f"Error cleaning up property setters: {str(e)}")
