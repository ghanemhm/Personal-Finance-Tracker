import csv
import sys
import webbrowser
import os
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


def generate_html_report(summary, transactions):
    expense_categories = {
        k: v for k, v in summary["category_totals"].items() if k != "Income"
    }
    sorted_cats = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
    cat_labels = [c[0] for c in sorted_cats]
    cat_values = [round(c[1], 2) for c in sorted_cats]

    # Group debits by month, get 2 most recent months' top 5
    monthly_debits = {}
    for t in transactions:
        if t["type"] == "Debit":
            key = t["date"].strftime("%Y-%m")
            monthly_debits.setdefault(key, []).append(t)
    recent_months = sorted(monthly_debits.keys(), reverse=True)[:2]
    recent_months.sort()  # chronological order

    monthly_top5 = []
    for month_key in recent_months:
        debits = sorted(monthly_debits[month_key], key=lambda x: x["amount"], reverse=True)[:5]
        label = datetime.strptime(month_key, "%Y-%m").strftime("%b %Y")
        monthly_top5.append({
            "label": label,
            "descriptions": [t["description"][:25] for t in debits],
            "amounts": [round(t["amount"], 2) for t in debits],
        })

    income = round(summary["total_income"], 2)
    expenses = round(summary["total_expenses"], 2)
    net = round(summary["net_balance"], 2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Finance Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; color: #333; }}
  h1 {{ text-align: center; margin-bottom: 24px; }}
  .cards {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 32px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 20px 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; min-width: 160px; }}
  .card .label {{ font-size: 14px; color: #777; margin-bottom: 4px; }}
  .card .value {{ font-size: 28px; font-weight: 700; }}
  .card .income {{ color: #22c55e; }}
  .card .expense {{ color: #ef4444; }}
  .card .net {{ color: {"'#22c55e'" if summary['net_balance'] >= 0 else "'#ef4444'"}; }}
  .charts {{ display: flex; gap: 24px; flex-wrap: wrap; justify-content: center; }}
  .chart-box {{ background: #fff; border-radius: 10px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); width: 420px; max-width: 95vw; }}
  .chart-box h2 {{ font-size: 18px; margin: 0 0 16px; text-align: center; }}
</style>
</head>
<body>
<h1>Personal Finance Report</h1>

<div class="cards">
  <div class="card"><div class="label">Total Income</div><div class="value income">${income:,.2f}</div></div>
  <div class="card"><div class="label">Total Expenses</div><div class="value expense">${expenses:,.2f}</div></div>
  <div class="card"><div class="label">Net Balance</div><div class="value net">${net:,.2f}</div></div>
  <div class="card"><div class="label">Transactions</div><div class="value">{summary['transaction_count']}</div></div>
</div>

<div class="charts">
  <div class="chart-box"><h2>Spending by Category</h2><canvas id="doughnut"></canvas></div>
  <div class="chart-box"><h2>Income vs Expenses</h2><canvas id="incexp"></canvas></div>
{"".join(f'  <div class="chart-box"><h2>Top 5 Expenses &mdash; {m["label"]}</h2><canvas id="top5_{i}"></canvas></div>' + chr(10) for i, m in enumerate(monthly_top5))}
</div>

<script>
const colors = ['#4f46e5','#f59e0b','#10b981','#ef4444','#8b5cf6','#ec4899','#06b6d4','#f97316','#6366f1','#14b8a6'];

new Chart(document.getElementById('doughnut'), {{
  type: 'doughnut',
  data: {{ labels: {cat_labels}, datasets: [{{ data: {cat_values}, backgroundColor: colors }}] }},
  options: {{ plugins: {{ legend: {{ position: 'bottom' }} }} }}
}});

new Chart(document.getElementById('incexp'), {{
  type: 'bar',
  data: {{ labels: ['Income','Expenses'], datasets: [{{ data: [{income},{expenses}], backgroundColor: ['#22c55e','#ef4444'] }}] }},
  options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
}});

{"".join(f"""new Chart(document.getElementById('top5_{i}'), {{{{
  type: 'bar',
  data: {{{{ labels: {m['descriptions']}, datasets: [{{{{ data: {m['amounts']}, backgroundColor: '#4f46e5' }}}}] }}}},
  options: {{{{ indexAxis: 'y', plugins: {{{{ legend: {{{{ display: false }}}} }}}}, scales: {{{{ x: {{{{ beginAtZero: true }}}} }}}} }}}}
}}}});
""" for i, m in enumerate(monthly_top5))}
</script>
</body>
</html>"""

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    return report_path


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

    report_path = generate_html_report(summary, transactions)
    print(f"\n  HTML report saved to: {report_path}")
    webbrowser.open("file://" + report_path.replace("\\", "/"))


if __name__ == "__main__":
    main()
