# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Frappe Lending Application Overview

This is a Frappe Framework application for comprehensive loan management system (LMS) built on top of ERPNext. The app streamlines the entire loan lifecycle from origination to closure for financial institutions, NBFCs, and lenders.

### Application Structure

The lending app follows standard Frappe Framework conventions with a single module called "Loan Management" containing all loan-related functionality:

```
lending/
├── loan_management/          # Main module
│   ├── doctype/             # 50+ loan-related document types
│   ├── report/              # Financial and operational reports
│   ├── dashboard_chart/     # Chart configurations
│   ├── number_card/         # KPI cards for dashboards
│   └── workspace/           # Workspace configuration
├── overrides/               # ERPNext DocType extensions
├── patches/                 # Database migration scripts
├── public/                  # Frontend assets (JS/CSS)
├── templates/               # Custom templates
├── tests/                   # Test utilities
└── translations/            # Multi-language support (40+ languages)
```

## Essential Development Commands

### Basic Operations
```bash
# Install the lending app (if not already installed)
bench --site [site-name] install-app lending

# Build and reload after code changes
bench build --app lending
bench --site [site-name] reload-doc lending loan_management [doctype-name] --force

# Clear cache after changes
bench --site [site-name] clear-cache

# Start development server
bench start
```

### Testing Commands
```bash
# Run all lending app tests
bench run-tests --app lending

# Run specific test file (must be in tests folder)
bench run-tests --module lending.loan_management.tests.test_loan

# Run tests with coverage
bench run-tests --app lending --coverage

# Run specific test method
bench run-tests --module lending.loan_management.tests.test_loan.TestLoan.test_loan_with_security

# Additional test modules in proper location
bench run-tests --module lending.loan_management.tests.test_loan_product
bench run-tests --module lending.loan_management.tests.test_loan_disbursement
```

### Database Operations
```bash
# Force reload specific DocType after JSON changes
bench --site [site-name] reload-doc lending loan_management loan --force

# Run lending-specific patches
bench --site [site-name] migrate

# Console for debugging
bench --site [site-name] console
```

## Core Architecture Components

### Key DocTypes and Their Relationships

**Core Loan Flow:**
1. **Loan Application** → **Loan** → **Loan Disbursement** → **Loan Repayment** → **Loan Write Off** (if needed)

**Main DocTypes:**
- **Loan**: Central document managing loan lifecycle
- **Loan Product**: Templates defining loan terms and conditions
- **Loan Application**: Initial loan request and approval workflow
- **Loan Security**: Collateral management for secured loans
- **Loan Disbursement**: Fund disbursement tracking
- **Loan Repayment**: Payment processing and schedule management
- **Loan Interest Accrual**: Interest calculation and booking

**Configuration DocTypes:**
- **Loan Category**: Loan classification system
- **Loan Partner**: Co-lending and loan transfer partners
- **Loan Classification**: Asset classification (standard, special mention, sub-standard, etc.)

### Automated Processes (Scheduled Tasks)

The app includes several automated daily/monthly processes defined in `hooks.py`:
- **Interest Accrual**: Daily interest calculation
- **Loan Demand**: Demand generation for due amounts
- **Security Shortfall**: Monitoring collateral value changes
- **Loan Classification**: Asset quality classification updates
- **Auto Closure**: Automatic closure for fully paid loans

### Key Features Implemented

1. **Flexible Loan Products**: Customizable terms, interest rates, repayment schedules
2. **Security Management**: Pledging, unpledging, shortfall tracking
3. **Interest Calculations**: Multiple methods (flat, reducing balance, compound)
4. **Demand Management**: Automated billing with collection sequences
5. **Asset Classification**: RBI-compliant loan classification system
6. **Co-lending Support**: Partner-based loan sharing and transfers
7. **Financial Integration**: Complete GL entries for all transactions

## Development Patterns

### Custom Field Management (MANDATORY)

#### Naming Convention
All custom fields created by lending MUST follow this naming pattern:
- **App Name**: lending  
- **Prefix**: `lending_custom_`
- **Pattern**: `lending_custom_{descriptive_field_name}`
- **Label**: Can be human-readable without prefix

```python
# CORRECT - Following naming convention
"Customer": [
    {
        "fieldname": "lending_custom_credit_limit_amount",
        "label": "Credit Limit Amount",
        "fieldtype": "Currency",
        "precision": 2,
        "insert_after": "customer_type"
    }
]

# INCORRECT - Missing prefix (legacy fields, to be migrated)
"Customer": [
    {
        "fieldname": "credit_limit_amount",  # Missing lending_custom_ prefix
        "label": "Credit Limit Amount",
        "fieldtype": "Currency",
        "precision": 2,
        "insert_after": "customer_type"
    }
]
```

**Note**: Some legacy fields may not follow this convention yet. New fields MUST use the `lending_custom_` prefix, and existing fields should be migrated when modified.

### Test Folder Structure (MANDATORY)
All test files MUST be placed in the designated tests folder following ERPNext standards:

```
lending/
├── loan_management/
│   └── tests/                    # MANDATORY test folder location
│       ├── __init__.py          # Required for Python module
│       ├── test_loan.py         # Core loan functionality tests
│       ├── test_loan_product.py # Loan product configuration tests
│       ├── test_loan_application.py     # Application workflow tests
│       ├── test_loan_disbursement.py   # Disbursement process tests
│       ├── test_loan_repayment.py      # Repayment processing tests
│       └── test_loan_security.py       # Collateral management tests
└── tests/                       # App-level test utilities (if needed)
    ├── __init__.py
    └── test_utilities.py
```

**Reference Standard**: Follow `apps/erpnext/erpnext/tests` structure as documented in Documentation/rules.md

**Rules**:
1. **All test files** MUST be in `app_name/module_name/tests/` folder
2. **Test files** MUST start with `test_` prefix
3. **Each module** can have its own tests subfolder if complex
4. **Import pattern**: `from lending.loan_management.tests.test_module import TestClass`

### DocType Development Workflow
1. Create new DocTypes via Frappe's GUI-based Form Builder
2. Export fixtures to get JSON definitions
3. Place JSON files in appropriate `doctype/` directory
4. Create corresponding Python controller class
5. Add business logic validation in the Python class
6. Write comprehensive unit tests

### Custom Field Integration
If extending ERPNext DocTypes with loan-related fields:
```python
# In hooks.py - customize ERPNext documents
doc_events = {
    "Sales Invoice": {
        "on_submit": "lending.overrides.sales_invoice.generate_demand",
        "validate": "lending.overrides.sales_invoice.validate"
    }
}
```

### Accounting Integration
All loan transactions automatically create General Ledger entries through ERPNext's accounting framework:
- Loan disbursements create asset entries
- Interest accrual creates income entries
- Repayments reduce loan balances
- Write-offs create expense entries

## Code Quality and Standards

### Python Standards
- Follow Frappe Framework coding conventions
- Use type hints (enabled via `export_python_type_annotations = True`)
- Code formatting: 99 character line length (configured in pyproject.toml)
- Import organization using isort with Frappe-specific sections

### Testing Standards
- Minimum 85% code coverage (codecov.yml configuration)
- Unit tests for all business logic
- Integration tests for complex workflows
- Test data setup using Frappe's test utilities

#### Test Structure Example
```python
# lending/loan_management/tests/test_loan.py
import frappe
import unittest
from frappe.tests.utils import FrappeTestCase

class TestLoan(unittest.TestCase):  # or FrappeTestCase
    def setUp(self):
        # Test setup for loan functionality
        self.company = frappe.get_doc("Company", "Test Company")
        pass
    
    def test_loan_creation(self):
        """Test loan creation with basic validation"""
        loan = frappe.get_doc({
            "doctype": "Loan",
            "applicant": "Test Customer",
            "loan_product": "Personal Loan", 
            "loan_amount": 100000,
            "company": "Test Company"
        })
        loan.insert()
        self.assertEqual(loan.loan_amount, 100000)
    
    def test_interest_calculation(self):
        """Test loan interest calculation methods"""
        loan = frappe.get_doc("Loan", "TEST-LOAN-001")
        interest = loan.calculate_interest(principal=100000, rate=12, period=1)
        self.assertEqual(interest, 10000)  # Simple interest calculation
    
    def tearDown(self):
        # Clean up test data
        pass
```

### Asset Management
- JavaScript files must use `.bundle.js` extension in hooks.py
- CSS files must use `.bundle.css` extension in hooks.py
- Frontend built using ESBuild pipeline

## CI/CD Pipeline

### Automated Testing
- GitHub Actions workflow in `.github/workflows/ci.yml`
- Tests run on Python 3.10 with MariaDB 11.3
- Code coverage reporting via Codecov
- Linting checks for code quality

### Deployment Considerations
- Requires ERPNext as dependency
- Uses standard Frappe bench deployment
- Database migrations handled via patches system
- Multi-language support via translation files

## Integration Points

### ERPNext Dependencies
The app extends several ERPNext DocTypes:
- **Company**: Loan account configuration
- **Sales Invoice**: Loan charge billing integration
- **Journal Entry**: Loan adjustments and transfers
- **Customer/Employee**: Loan applicant management

### External Integrations
- Bank reconciliation for loan payments
- Asset classification based on financial norms
- Multi-currency support for international loans
- Audit trail compliance for financial regulations

## Common Development Scenarios

### Adding New Loan Types
1. Create new Loan Product with specific configuration
2. Extend validation logic in Loan DocType if needed
3. Add any specific business rules in hooks.py
4. Update reports if new fields are required

### Modifying Interest Calculations
1. Update `Process Loan Interest Accrual` DocType
2. Modify calculation logic in the corresponding Python file
3. Add comprehensive tests for new calculation methods
4. Update existing loans if retroactive changes needed

### Custom Reporting
1. Create new report in `report/` directory
2. Use Frappe's query-builder for database queries
3. Add proper filters and formatting
4. Include in workspace configuration if needed

## Performance Considerations

- Loan interest accrual runs as daily scheduled job
- Large loan portfolios may require batch processing
- Index optimization for loan search and reporting
- Efficient GL entry creation for high-volume transactions

## Security and Compliance

- Role-based permissions for loan operations
- Audit trail for all loan modifications
- Data encryption for sensitive information
- Compliance with financial regulations (configurable)

This app provides a robust foundation for loan management with extensive customization capabilities through Frappe Framework's metadata-driven architecture.

---

## Development Rules & Standards

### Custom Field Naming Convention (MANDATORY)
Following [Documentation/rules.md](/home/frappe/frappe-bench/Documentation/rules.md):

- **App Name**: lending
- **Prefix**: `ld_custom_` (suggested lending prefix)
- **Pattern**: `ld_custom_{descriptive_field_name}`

#### Examples
```python
# ✅ CORRECT - Following naming convention
custom_field = {
    "fieldname": "ld_custom_collateral_type",
    "fieldtype": "Select",
    "label": "Collateral Type"
}

# ❌ INCORRECT - Missing app-specific prefix
custom_field = {
    "fieldname": "collateral_type",  # Should be ld_custom_collateral_type
    "fieldtype": "Select",
    "label": "Collateral Type"
}
```

### Testing Standards
- **Test Location**: `lending/lending/tests/`
- **Reference**: Follow `apps/erpnext/erpnext/tests` structure
- **Docs**: https://docs.frappe.io/framework/user/en/testing

### Uninstall Compliance
- **Requirement**: All custom fields MUST be removed during app uninstallation
- **Implementation**: Add `before_uninstall` hook in `hooks.py`
- **Reference Issue**: https://github.com/frappe/frappe/issues/24108

#### Current Status
✅ **Note**: Lending is a standard ERPNext app that primarily uses custom DocTypes. If any custom fields exist, they should follow the `ld_custom_` naming convention.

### File Creation Guidelines
- Scan relevant files before creating new ones to prevent redundancy
- Check hooks.py regularly for duplicated functions or redundancy
- Follow ERPNext Custom Field Guidelines consistently

### Priority Compliance Items
1. **Review existing custom fields** (if any) and update naming to use `ld_custom_` prefix
2. **Add uninstall functionality** to clean up all custom fields (if any exist)
3. **Maintain test structure** following ERPNext standards
4. **Review hooks.py** for any redundancy

---

## Installation and Custom Fields

### Install.py Overview
The `lending/install.py` file manages the installation and integration of the lending app with ERPNext by adding custom fields to existing DocTypes.

### Custom Fields Added During Installation

The app adds loan-related custom fields to 6 core ERPNext DocTypes via `LOAN_CUSTOM_FIELDS` dictionary:

#### 1. **Sales Invoice** (4 fields)
- `loan`: Link to Loan document
- `loan_disbursement`: Link to Loan Disbursement (read-only)
- `loan_repayment`: Link to Loan Repayment (read-only)
- `value_date`: Date field for transaction dating

#### 2. **Company** (19 fields in Loan Tab)
Comprehensive loan configuration including:
- **Loan Settings Section**:
  - `loan_restructure_limit`: Overall restructure limit percentage
  - `watch_period_post_loan_restructure_in_days`: Watch period after restructuring
  - `interest_day_count_convention`: Options (Actual/365, 30/360, etc.)
  - `min_days_bw_disbursement_first_repayment`: Minimum days between disbursement and first repayment
  - `loan_accrual_frequency`: Daily/Weekly/Monthly options
- **Collection Configuration**:
  - `collection_offset_logic_based_on`: NPA Flag or Days Past Due
  - `days_past_due_threshold`: Threshold for overdue status
  - `days_past_due_threshold_for_auto_write_off`: Auto write-off threshold
  - Collection offset sequences for different asset classifications
- **Classification Tables**:
  - `loan_classification_ranges`: Table for loan classification configuration
  - `irac_provisioning_configuration`: IRAC provisioning setup

#### 3. **Customer** (2 fields)
- `loan_details_tab`: Tab break for loan information
- `is_npa`: Non-Performing Asset flag

#### 4. **Item Default** (6 fields)
Loan-specific default accounts:
- `default_receivable_account`: Receivable account for loan items
- `default_waiver_account`: Account for loan waivers
- `default_write_off_account`: Write-off account
- `default_suspense_account`: Suspense account for unallocated payments

#### 5. **Journal Entry** (3 fields)
- `loan_transfer`: Link to Loan Transfer document
- `loan`: Link to Loan document
- `value_date`: Date field for value dating

#### 6. **GL Entry** (1 field)
- `value_date`: Date field for general ledger value dating

### Installation Functions

- **`after_install()`**: Creates all custom fields and configures Journal Entry reference types
- **`make_property_setter_for_journal_entry()`**: Adds "Loan Interest Accrual" as a valid reference type
- **`before_uninstall()`**: Properly removes all custom fields on app uninstallation
- **`delete_custom_fields()`**: Helper function for clean field removal

### ⚠️ IMPORTANT: Naming Convention Issue

**Current Status**: The custom fields in `install.py` DO NOT follow the recommended naming convention. They use generic names like "loan", "value_date" instead of the required `ld_custom_` or `lending_custom_` prefix.

**Action Required**: 
- All new custom fields MUST use `ld_custom_` prefix
- Existing fields should be migrated when modified
- This is critical for preventing field name conflicts with other apps

### ✅ Good Practices Implemented

1. **Proper Uninstall**: The app correctly implements `before_uninstall()` to clean up custom fields
2. **Property Setter Management**: Properly extends Journal Entry reference types
3. **Field Organization**: Logical grouping with sections and tabs for better UX
4. **ERPNext Field Positioning Fix**: Includes `fix_column_break_32_position()` to ensure `column_break_32` stays in stock_tab with proper `insert_after` property

### Field Positioning Fix

The lending app includes a critical fix for ERPNext's `column_break_32` field positioning issue:

**Problem**: `column_break_32` (an ERPNext stock_tab field) was appearing in loan_tab due to missing `insert_after` property.

**Solution**: Added `fix_column_break_32_position()` function that:
- Checks if Property Setter exists for `column_break_32`
- Creates/updates Property Setter to set `insert_after = "default_in_transit_warehouse"`
- Ensures stable field positioning using `make_property_setter()` method

**Result**: 
- `column_break_32` correctly positioned in stock_tab after `default_in_transit_warehouse`
- `manufacturing_section` and `default_operating_cost_account` remain in correct positions
- `loan_tab` appears after all stock fields as intended

This fix prevents field layout issues that could affect other apps using Company DocType.