'''
    
def budgetQuarterPerformance(budgetId: str) -> dict:
    """
    Analyzes budget performance per quarter with statistical metrics
    Returns: {
        "quarterId1": {
            "disbursed": float,
            "expended": float,
            "variance": float,
            "std_dev": float,
            "item_behavior": dict,
            "budget_performance": dict
        },
        ...
    }
    """
    # Get quarter data
    qd = db.getQuartersByBudgetId(budgetId)
    if not qd['status']:
        return {"error": qd['log']}
    
    # Initialize results dictionary
    performance_results = {}
    
    # Convert to DataFrame for statistical calculations
    quarters_df = pd.DataFrame(qd['data'])
    
    for _, quarter in quarters_df.iterrows():
        quarter_id = quarter['quaterId']
        quarter_results = analyze_quarter_performance(budgetId, quarter_id)
        performance_results[quarter_id] = quarter_results
    
    # Add cross-quarter statistical analysis
    add_cross_quarter_analysis(performance_results)
    
    return performance_results

def analyze_quarter_performance(budgetId: str, quarterId: str) -> dict:
    """Analyzes performance for a single quarter with statistical metrics"""
    # Get financial data
    dsbR = db.getDisbursementsByBudgetQuarter(budgetId, quarterId)
    expR = db.getExpendituresByBudgetQuarter(budgetId, quarterId)
    
    # Convert to DataFrames
    disbursements = pd.DataFrame(dsbR['data']) if dsbR['status'] else pd.DataFrame()
    expenditures = pd.DataFrame(expR['data']) if expR['status'] else pd.DataFrame()
    
    # Initialize results
    results = {
        "disbursed": 0.0,
        "expended": 0.0,
        "variance": None,
        "std_dev": None,
        "item_behavior": {},
        "budget_performance": {}
    }
    
    # Calculate disbursements
    if not disbursements.empty:
        results["disbursed"] = disbursements['amountReleased'].sum()
        
    # Calculate expenditures with variance/std
    if not expenditures.empty:
        # Expand expenditure items
        exp_items = []
        for _, row in expenditures.iterrows():
            details = row['detailsOfExpense']
            for i in range(len(details['items'])):
                exp_items.append({
                    'item': details['items'][i],
                    'amount': details['amount'][i] * details['quantity'][i],
                    'unit_price': details['amount'][i],
                    'quantity': details['quantity'][i]
                })
        
        exp_df = pd.DataFrame(exp_items)
        results["expended"] = exp_df['amount'].sum()
        
        # Calculate variance and std dev
        if len(exp_df) > 1:
            results["variance"] = exp_df['amount'].var()
            results["std_dev"] = exp_df['amount'].std()
        
        # Item behavior analysis
        planned_items = get_planned_items(budgetId, quarterId)
        if planned_items:
            actual_items = exp_df.groupby('item')['amount'].sum().to_dict()
            results["item_behavior"] = utils.getItemExpendutureBehaviour(
                proposedItemDetails={'itemTotals': planned_items},
                actualItemDetails={'itemTotals': actual_items}
            )
        
        # Budget performance
        results["budget_performance"] = utils.getOverallPercentages(
            budgetAmount={'workingAmount': results["disbursed"]},
            expenditureAmount={'totalExpenses': results["expended"]}
        )
    
    return results

def add_cross_quarter_analysis(performance_data: dict):
    """Adds cross-quarter statistical analysis"""
    quarters = list(performance_data.keys())
    disbursed = [v['disbursed'] for v in performance_data.values()]
    expended = [v['expended'] for v in performance_data.values()]
    
    if len(quarters) > 1:
        # Calculate trends across quarters
        disbursed_series = pd.Series(disbursed)
        expended_series = pd.Series(expended)
        
        for i, q in enumerate(quarters):
            performance_data[q].update({
                "disbursed_trend": None if i == 0 else disbursed[i] - disbursed[i-1],
                "expended_trend": None if i == 0 else expended[i] - expended[i-1],
                "disbursed_rolling_avg": disbursed_series[:i+1].mean() if i > 0 else None,
                "expended_rolling_avg": expended_series[:i+1].mean() if i > 0 else None
            })

def get_planned_items(budgetId: str) -> dict:
    """
    Retrieves original planned items/amounts by multiplying quantity × amount
    from the budget's detailsOfBudget field.
    
    Args:
        budgetId: The budget ID to lookup
        
    Returns:
        {
            "Essential Medicines": 2,500,000,  # 100,000 × 25
            "Hospital Equipment": 2,000,000,   # 50 × 40,000
            "Staff Salaries": 1,800,000        # 120 × 15,000
        }
        or empty dict if no data
    """
    # 1. Get the budget data
    budget = db.getPalnnedByBudgetId(budgetId)
    if not budget.get('status') or not budget['data']:
        return {}
    
    # 2. Extract and calculate planned amounts
    details = budget['data'][0]['detailsOfBudget']  # Access first record's details
    planned = {}
    
    for i in range(len(details['items'])):
        item_name = details['items'][i]
        total = details['quantity'][i] * details['amount'][i]
        planned[item_name] = total
    
    return planned

'''

import db
import utils
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import os
quarters_education = [
    {
        "budgetId": "bIDvWU6mkod",  # Your provided ID
        "quaterId": "Q1-2023",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31",
        "others": {
            "plannedRelease": 1_000_000,  # Matches releaseHistory
            "actualRelease": 1_000_000,
            "releaseEvidence": "TR-Q1-EDU-2023.pdf",
            "notes": "Full release for textbook procurement"
        }
    },
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q2-2023",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30",
        "others": {
            "plannedRelease": 1_000_000,
            "actualRelease": 900_000,  # Matches releaseHistory (10% withheld)
            "releaseEvidence": "TR-Q2-EDU-2023.pdf",
            "notes": "Withheld 100K pending delivery verification"
        }
    },
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q3-2023",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30",
        "others": {
            "plannedRelease": 1_000_000,
            "actualRelease": 700_000,  # Matches releaseHistory
            "releaseEvidence": "TR-Q3-EDU-2023.pdf",
            "notes": "Partial release for teacher training"
        }
    },
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q4-2023",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31",
        "others": {
            "plannedRelease": 800_000,
            "actualRelease": 300_000,  # Matches releaseHistory
            "releaseEvidence": "TR-Q4-EDU-2023.pdf",
            "notes": "Year-end budget cuts applied"
        }
    }
]

disbursements_education = [
    # Q1 2023 - Textbook Procurement (Full Release)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q1-2023",
        "disbursementDate": "2023-03-12",
        "amountReleased": 1_000_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "John O. (FIN-EDU-001)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q1-2023.pdf",
        "others": {
            "purpose": "Textbook printing and distribution",
            "bankRef": "BNK-EDU-0323",
            "itemsCovered": ["Textbooks"],
            "supplier": "National Printing Press"
        }
    },
    # Q2 2023 - Science Kits (Partial Release)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q2-2023",
        "disbursementDate": "2023-06-18",
        "amountReleased": 900_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Sarah M. (FIN-EDU-002)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q2-2023.pdf",
        "others": {
            "purpose": "Science lab equipment for 150 schools",
            "chequeNo": "CHQ-EDU-456789",
            "itemsCovered": ["Science Kits"],
            "withheldAmount": 100_000,
            "withheldReason": "Pending delivery verification"
        }
    },
    # Q3 2023 - Teacher Training (Partial Release)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q3-2023",
        "disbursementDate": "2023-09-08",
        "amountReleased": 700_000,
        "paymentMethod": "Mobile Money",
        "disbursementOfficer": "David K. (FIN-EDU-003)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q3-2023.pdf",
        "others": {
            "purpose": "Teacher training workshops",
            "mobileRef": "MM-EDU-789123",
            "itemsCovered": ["Teacher Training"],
            "beneficiaries": ["Teachers College A", "Teachers College B"],
            "attendees": 75
        }
    },
    # Q4 2023 - Final Partial Release
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q4-2023",
        "disbursementDate": "2023-12-03",
        "amountReleased": 300_000,
        "paymentMethod": "Wire Transfer",
        "disbursementOfficer": "Grace L. (FIN-EDU-004)",
        "department": "Education",
        "status": "Pending",
        "evidence": "VOUCHER-EDU-Q4-2023.pdf",
        "others": {
            "purpose": "School maintenance grants",
            "swiftCode": "UGEDUGKA",
            "itemsCovered": ["Textbooks", "Science Kits"],
            "notes": "Reduced due to budget cuts"
        }
    }
]

expenditures_education = [
    # Q1 2023 - Textbook Distribution (Materials)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q1-2023",
        "dateOfExpense": "2023-03-25",
        "amountSpent": 950_000,
        "detailsOfExpense": {
            "items": ["Primary Math Text", "Science Readers"],  # Names can vary
            "quantity": [40000, 10000],  # Total 50,000 books (matches budget)
            "amount": [20, 15],  # Unit prices (different from budget is okay)
            "categories": ["Materials", "Materials"]  # Must match budget
        },
        "beneficially": "District Schools Board",
        "description": "Q1 Textbook distribution to 120 schools",
        "evidence": "EXP-EDU-Q1-2023.pdf",
        "others": {
            "disbursementRef": "dIDeduQ1",  # Link to Q1 disbursement
            "schoolsCovered": 120,
            "deliveryNote": "DN-EDU-0325"
        }
    },
    # Q2 2023 - Science Equipment (Equipment)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q2-2023",
        "dateOfExpense": "2023-06-30",
        "amountSpent": 850_000,
        "detailsOfExpense": {
            "items": ["Chemistry Sets", "Physics Lab Kits"],
            "quantity": [100, 50],  # Total 150 kits (matches Q2 target)
            "amount": [5000, 7000],
            "categories": ["Equipment", "Equipment"]  # Consistent
        },
        "beneficially": "Science Teachers Association",
        "description": "Lab equipment for 150 schools",
        "evidence": "EXP-EDU-Q2-2023.pdf",
        "others": {
            "disbursementRef": "dIDeduQ2",
            "warrantyPeriod": "2 years"
        }
    },
    # Q3 2023 - Teacher Workshops (Training)
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q3-2023",
        "dateOfExpense": "2023-09-20",
        "amountSpent": 650_000,
        "detailsOfExpense": {
            "items": ["Pedagogy Training", "STEM Workshops"],
            "quantity": [70, 5],  # 70 teachers, 5 workshop sessions
            "amount": [8000, 18000],
            "categories": ["Training", "Training"]  # As per budget
        },
        "beneficially": "National Teachers Union",
        "description": "Q3 Professional development",
        "evidence": "EXP-EDU-Q3-2023.pdf",
        "others": {
            "disbursementRef": "dIDeduQ3",
            "trainers": ["Dr. Smith", "Prof. Johnson"]
        }
    },
    # Q4 2023 - Final Expenditures
    {
        "budgetId": "bIDvWU6mkod",
        "quaterId": "Q4-2023",
        "dateOfExpense": "2023-12-15",
        "amountSpent": 250_000,
        "detailsOfExpense": {
            "items": ["Repaired Textbooks", "Lab Consumables"],
            "quantity": [5000, 200],
            "amount": [30, 500],
            "categories": ["Materials", "Equipment"]  # Mixed but valid
        },
        "beneficially": "Vocational Schools",
        "description": "Year-end maintenance and supplies",
        "evidence": "EXP-EDU-Q4-2023.pdf",
        "others": {
            "disbursementRef": "dIDeduQ4",
            "emergencyAllocation": True
        }
    }
]
budgets = [
    {
        # Health Ministry Budget (FY 2023)
        "dateOfApproval": "2023-01-10",
        "planned": 6_350_000,  # Total planned (100000*25 + 50*40000 + 120*15000)
        "working": 4_200_000,  # Actual released (66.1% of planned)
        "department": "Health",
        "programme": "Primary Healthcare",
        "vote": "VOTE-2023-HEALTH",
        "detailsOfBudget": {
            "items": ["Essential Medicines", "Hospital Equipment", "Staff Salaries"],
            "quantity": [100000, 50, 120],
            "amount": [25, 40000, 15000],  # Unit prices
            "categories": ["Drugs", "Assets", "Personnel"]
        },
        "description": "2023 Health Budget - Revised per Parliament Approval",
        "others": {
            "releaseHistory": [
                {"quarter": "Q1", "amount": 1_500_000, "date": "2023-03-15"},
                {"quarter": "Q2", "amount": 1_200_000, "date": "2023-06-20"},
                {"quarter": "Q3", "amount": 1_000_000, "date": "2023-09-10"},
                {"quarter": "Q4", "amount": 500_000, "date": "2023-12-05"}  # Partial release
            ],
            "approvalRef": "FIN/HEALTH/2023/001"
        }
    },
    {
        # Education Ministry Budget (FY 2023)
        "dateOfApproval": "2023-01-10",
        "planned": 3_800_000,  # Total planned (50000*10 + 200*1500 + 80*20000)
        "working": 2_900_000,  # Actual released (76.3% of planned)
        "department": "Education",
        "programme": "Secondary Schools",
        "vote": "VOTE-2023-EDU",
        "detailsOfBudget": {
            "items": ["Textbooks", "Science Kits", "Teacher Training"],
            "quantity": [50000, 200, 80],
            "amount": [10, 1500, 20000],
            "categories": ["Materials", "Equipment", "Training"]
        },
        "description": "2023 National Education Budget",
        "others": {
            "releaseHistory": [
                {"quarter": "Q1", "amount": 1_000_000, "date": "2023-03-10"},
                {"quarter": "Q2", "amount": 900_000, "date": "2023-06-15"},
                {"quarter": "Q3", "amount": 700_000, "date": "2023-09-05"},
                {"quarter": "Q4", "amount": 300_000, "date": "2023-12-01"}  # Partial release
            ],
            "approvalRef": "FIN/EDU/2023/001"
        }
    }
]






def plot_quarterly_pies_detailed(budgetId: str, output_dir: str):
    """
    Generates detailed pie charts for each quarter showing:
    1. Planned vs Expended (amounts and %)
    2. Category contributions (amounts, %, and item details)
    
    Saves each quarter's chart as a PNG in the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Get metrics
    data = utils.getQuarterlyPerfromanceMetric(budgetId)
    if "error" in data:
        raise ValueError(f"Error getting quarterly metrics: {data['error']}")
    
    for quarter_id, quarter_data in data.items():
        # ---- Financial Data ----
        planned = quarter_data["financial"]["planned"]
        expended = quarter_data["financial"]["expended"]
        remaining = max(planned - expended, 0)
        
        # ---- Category Analysis ----
        category_analysis = quarter_data["category_analysis"]
        category_labels = []
        category_actuals = []
        
        for category, cat_data in category_analysis.items():
            # Build label with category name, variance, and items
            label_lines = [f"{category} (Var: {cat_data['variance']:.2f})"]
            
            for item_name, item_data in cat_data["items"].items():
                label_lines.append(f"  {item_name}: {item_data['actual']:.2f}")
            
            category_labels.append("\n".join(label_lines))
            category_actuals.append(cat_data["actual"])
        
        # ---- Create Figure ----
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))
        
        # Pie 1: Quarter Performance (Planned vs Expended)
        def autopct_format(values):
            def inner_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f"{pct:.1f}%\n({val:,})"
            return inner_autopct
        
        axes[0].pie(
            [expended, remaining],
            labels=["Expended", "Remaining"],
            autopct=autopct_format([expended, remaining]),
            colors=["#4CAF50", "#FFC107"],
            startangle=90
        )
        axes[0].set_title(f"{quarter_id} - Performance (Planned vs Expended)")
        
        # Pie 2: Category Contributions (with item details)
        wedges, texts, autotexts = axes[1].pie(
            category_actuals,
            labels=category_labels,
            autopct=autopct_format(category_actuals),
            startangle=90
        )
        for text in texts:
            text.set_fontsize(8)  # Smaller font for multi-line category labels
        for autotext in autotexts:
            autotext.set_fontsize(8)
        
        axes[1].set_title(f"{quarter_id} - Category Contributions (Amounts & %)")
        
        plt.tight_layout()
        
        # Save to file
        output_path = os.path.join(output_dir, f"{quarter_id}_detailed_pie_chart.png")
        plt.savefig(output_path, dpi=300)
        plt.close()
        print(f"Saved detailed pie chart for {quarter_id} to {output_path}")



if __name__ == "__main__":
    
    # pprint.pprint(budgetQuaterPerformance("bIDziMnNLhw"))
    # for quater in expenditures_education:
        # print(db.insertDataIntoExpenditure(quater))
    # pprint.pprint(db.getExpendituresByBudgetQuarter("bIDvWU6mkod","qId7MFFvF"))
    # pprint.pprint(db.getQuartersByBudgetId('bIDvWU6mkod'))
    
    # pprint.pprint(db.getAnyTableData({
    #     'tableName': 'budget',
    #     'columns': ['*'],
    #     'condition': 'budgetId = ?',
    #     'conditionalData': ["bIDvWU6mkod"],
    #     'limit':100,
    #     'returnDicts': True,
    #     'returnNamespaces': False,
    #     'parseJson': True,
    #     'returnGenerator': False 
        
    # })    )
    metrics = utils.getQuarterlyPerfromanceMetric('bIDziMnNLhw')
    # plot_quarterly_pies_detailed('bIDvWU6mkod','/workspaces/budgetMornitoringSystem/budgetMonitoring/database')
    pprint.pprint(metrics)
    # print(plot_quarterly_activities(metrics,save_path='quarterly_performance.png'))
        # pass