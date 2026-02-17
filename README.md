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

  Total Income:    $ 15,800.00
  Total Expenses:  $  7,492.05
  Net Balance:     $  8,307.95
  Transactions:            48

-------------------------------------------------------
  SPENDING BY CATEGORY
-------------------------------------------------------
  Housing          $ 5,400.00  ( 72.1%)  ####################################
  Groceries        $   572.45  (  7.6%)  ###
  Shopping         $   554.70  (  7.4%)  ###
  Utilities        $   492.49  (  6.6%)  ###
  Transportation   $   222.60  (  3.0%)  #
  Dining           $   143.85  (  1.9%)
  Entertainment    $   105.96  (  1.4%)

-------------------------------------------------------
  TOP 5 LARGEST EXPENSES
-------------------------------------------------------
  1. 2026-01-29  Mortgage Payment             $ 1,500.00
  2. 2026-02-16  Mortgage Payment             $ 1,500.00
  3. 2026-01-09  Rent Payment                 $ 1,200.00
  4. 2026-02-02  Rent Payment                 $ 1,200.00
  5. 2026-01-25  Best Buy Electronics         $   199.99

=======================================================
```

## Requirements

Python 3.6+ (no external dependencies — uses only stdlib).
