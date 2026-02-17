import csv
import sys
from datetime import datetime


CATEGORY_KEYWORDS = {
    "Groceries": ["walmart", "kroger", "trader joe", "whole foods", "grocery", "market"],
    "Dining": ["restaurant", "mcdonald", "starbucks", "pizza", "burger", "cafe", "coffee"],
    "Utilities": ["electric", "water", "gas bill", "internet", "phone bill", "utility"],
    "Transportation": ["uber", "lyft", "shell", "chevron", "parking", "gas station", "fuel"],
    "Entertainment": ["netflix", "spotify", "cinema", "steam", "hulu", "game"],
    "Housing": ["rent", "mortgage"],
    "Shopping": ["amazon", "target", "best buy", "ebay"],
    "Income": ["salary", "deposit", "transfer in", "payroll", "refund"],
}


def load_transactions(filepath):
    transactions = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": datetime.strptime(row["Date"].strip(), "%Y-%m-%d"),
                "description": row["Description"].strip(),
                "amount": float(row["Amount"].strip()),
                "type": row["Type"].strip(),
            })
    return transactions


def categorize_transaction(description):
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return "Other"


def categorize_all(transactions):
    for t in transactions:
        t["category"] = categorize_transaction(t["description"])
    return transactions


def generate_summary(transactions):
    total_income = 0.0
    total_expenses = 0.0
    category_totals = {}
    expenses_list = []

    for t in transactions:
        if t["type"] == "Credit":
            total_income += t["amount"]
        else:
            total_expenses += t["amount"]
            expenses_list.append(t)

        cat = t["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + t["amount"]

    expenses_list.sort(key=lambda x: x["amount"], reverse=True)

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
        "category_totals": category_totals,
        "top_expenses": expenses_list[:5],
        "transaction_count": len(transactions),
    }


def print_report(summary):
    print("=" * 55)
    print("         PERSONAL FINANCE REPORT")
    print("=" * 55)

    print(f"\n  Total Income:    ${summary['total_income']:>10,.2f}")
    print(f"  Total Expenses:  ${summary['total_expenses']:>10,.2f}")
    print(f"  Net Balance:     ${summary['net_balance']:>10,.2f}")
    print(f"  Transactions:    {summary['transaction_count']:>10}")

    print("\n" + "-" * 55)
    print("  SPENDING BY CATEGORY")
    print("-" * 55)

    expense_categories = {
        k: v for k, v in summary["category_totals"].items() if k != "Income"
    }
    total_exp = summary["total_expenses"]

    for cat, amount in sorted(expense_categories.items(), key=lambda x: x[1], reverse=True):
        pct = (amount / total_exp * 100) if total_exp > 0 else 0
        bar = "#" * int(pct / 2)
        print(f"  {cat:<16} ${amount:>9,.2f}  ({pct:5.1f}%)  {bar}")

    print("\n" + "-" * 55)
    print("  TOP 5 LARGEST EXPENSES")
    print("-" * 55)

    for i, t in enumerate(summary["top_expenses"], 1):
        date_str = t["date"].strftime("%Y-%m-%d")
        print(f"  {i}. {date_str}  {t['description']:<28} ${t['amount']:>9,.2f}")

    print("\n" + "=" * 55)


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "sample_bank_statement.csv"

    try:
        transactions = load_transactions(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    transactions = categorize_all(transactions)

    summary = generate_summary(transactions)
    print_report(summary)


if __name__ == "__main__":
    main()
