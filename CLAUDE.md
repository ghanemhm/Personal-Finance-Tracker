# Personal Finance Tracker

## Overview
A Python CLI tool that reads CSV bank statements, auto-categorizes transactions, and generates console spending reports.

## Usage
```
py finance_tracker.py [csv_file]
```
Defaults to `sample_bank_statement.csv` if no argument given.

## CSV Format
Files must have columns: `Date, Description, Amount, Type`
- Date format: `YYYY-MM-DD`
- Type: `Credit` or `Debit`

## Project Structure
- `finance_tracker.py` — Main script (loading, categorization, reporting)
- `sample_bank_statement.csv` — Sample data with ~29 transactions
- `CLAUDE.md` — This file

## Key Design Decisions
- Pure stdlib only (csv, sys, datetime) — no external dependencies
- Category matching is keyword-based via `CATEGORY_KEYWORDS` dict
- Unmatched transactions fall into "Other" category
- Run with `py` launcher on Windows (not `python`)

## Tasks

1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
