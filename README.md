# Personal Finance Tracker

A Python CLI tool that reads CSV bank statements, auto-categorizes transactions, and generates console spending reports.

## Features

- Reads any CSV with `Date, Description, Amount, Type` columns
- Auto-categorizes transactions using keyword matching (Groceries, Dining, Utilities, Transportation, Entertainment, Housing, Shopping, Income)
- Generates a formatted report with:
  - Total income, expenses, and net balance
  - Spending breakdown by category with percentage bars
  - Top 5 largest expenses

## Usage

```
py finance_tracker.py [csv_file]
```

Defaults to `sample_bank_statement.csv` if no file is specified.

## CSV Format

| Column      | Format              | Example              |
|-------------|---------------------|----------------------|
| Date        | `YYYY-MM-DD`        | `2026-01-15`         |
| Description | Free text           | `Walmart Grocery`    |
| Amount      | Decimal             | `87.32`              |
| Type        | `Credit` or `Debit` | `Debit`              |

## Sample Output

```
=======================================================
         PERSONAL FINANCE REPORT
=======================================================

  Total Income:    $  9,500.00
  Total Expenses:  $  3,973.71
  Net Balance:     $  5,526.29
  Transactions:            29

-------------------------------------------------------
  SPENDING BY CATEGORY
-------------------------------------------------------
  Housing          $ 2,700.00  ( 67.9%)  #################################
  Shopping         $   352.43  (  8.9%)  ####
  Groceries        $   347.97  (  8.8%)  ####
  Utilities        $   305.39  (  7.7%)  ###
  Transportation   $   136.70  (  3.4%)  #
  Entertainment    $    87.97  (  2.2%)  #
  Dining           $    43.25  (  1.1%)

-------------------------------------------------------
  TOP 5 LARGEST EXPENSES
-------------------------------------------------------
  1. 2026-01-29  Mortgage Payment             $ 1,500.00
  2. 2026-01-09  Rent Payment                 $ 1,200.00
  3. 2026-01-25  Best Buy Electronics         $   199.99
  4. 2026-01-07  Electric Bill Payment        $   125.40
  5. 2026-01-23  Whole Foods Market           $    95.40

=======================================================
```

## Requirements

Python 3.6+ (no external dependencies — uses only stdlib).
