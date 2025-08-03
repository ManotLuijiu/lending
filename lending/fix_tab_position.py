import frappe


def fix_loan_tab_position():
    """Fix the position of the loan_tab to not disrupt Stock and Manufacturing fields"""

    try:
        # Get the loan tab field
        loan_tab_name = frappe.db.get_value(
            "Custom Field", {"dt": "Company", "fieldname": "loan_tab"}, "name"
        )

        if not loan_tab_name:
            print("❌ loan_tab field not found")
            return False

        print(f"📝 Found loan tab field: {loan_tab_name}")

        # Check current position
        current_position = {
            "insert_after": frappe.db.get_value(
                "Custom Field", loan_tab_name, "insert_after"
            ),
            "idx": frappe.db.get_value("Custom Field", loan_tab_name, "idx"),
        }
        print(f"🔍 Current position: {current_position}")

        # Update the loan tab position to appear after hr_and_payroll_tab
        frappe.db.set_value(
            "Custom Field",
            loan_tab_name,
            {
                "insert_after": "hr_and_payroll_tab",
                "idx": 75,  # Set index between HR tab (0) and Stamps tab (200)
            },
        )

        frappe.db.commit()
        print("✅ Updated Loan tab position to appear after HR & Payroll tab")

        # Verify the change
        updated_tab = {
            "insert_after": frappe.db.get_value(
                "Custom Field", loan_tab_name, "insert_after"
            ),
            "idx": frappe.db.get_value("Custom Field", loan_tab_name, "idx"),
        }

        print(f"🔍 Verification - Loan tab now positioned: {updated_tab}")
        print(
            "\n🎯 This should fix the issue where 'Default Operating Cost Account' was appearing in Loan tab"
        )
        print("   instead of its proper location in Stock and Manufacturing section.")

        return True

    except Exception as e:
        print(f"❌ Error fixing loan tab position: {e}")
        frappe.db.rollback()
        return False
