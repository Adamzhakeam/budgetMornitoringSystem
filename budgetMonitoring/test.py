'''
hey this is a testing module     
'''

import db
import utils
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import os
quarters = [
    # Budget 1: bIDEyNOJYTT (Infrastructure)
    {
        "quaterId": "Q1-2023-bIDEyNOJYTT",
        "budgetId": "bIDEyNOJYTT",
        "name": "Q1 2023 - National Infrastructure",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31"
    },
    {
        "quaterId": "Q2-2023-bIDEyNOJYTT",
        "budgetId": "bIDEyNOJYTT",
        "name": "Q2 2023 - National Infrastructure",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30"
    },
    {
        "quaterId": "Q3-2023-bIDEyNOJYTT",
        "budgetId": "bIDEyNOJYTT",
        "name": "Q3 2023 - National Infrastructure",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30"
    },
    {
        "quaterId": "Q4-2023-bIDEyNOJYTT",
        "budgetId": "bIDEyNOJYTT",
        "name": "Q4 2023 - National Infrastructure",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31"
    },

    # Budget 2: bIDuIC1xEeG (Healthcare)
    {
        "quaterId": "Q1-2023-bIDuIC1xEeG",
        "budgetId": "bIDuIC1xEeG",
        "name": "Q1 2023 - Healthcare Enhancement",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31"
    },
    {
        "quaterId": "Q2-2023-bIDuIC1xEeG",
        "budgetId": "bIDuIC1xEeG",
        "name": "Q2 2023 - Healthcare Enhancement",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30"
    },
    {
        "quaterId": "Q3-2023-bIDuIC1xEeG",
        "budgetId": "bIDuIC1xEeG",
        "name": "Q3 2023 - Healthcare Enhancement",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30"
    },
    {
        "quaterId": "Q4-2023-bIDuIC1xEeG",
        "budgetId": "bIDuIC1xEeG",
        "name": "Q4 2023 - Healthcare Enhancement",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31"
    },

    # Budget 3: bIDQzxZp04C (Education)
    {
        "quaterId": "Q1-2023-bIDQzxZp04C",
        "budgetId": "bIDQzxZp04C",
        "name": "Q1 2023 - Education Transformation",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31"
    },
    {
        "quaterId": "Q2-2023-bIDQzxZp04C",
        "budgetId": "bIDQzxZp04C",
        "name": "Q2 2023 - Education Transformation",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30"
    },
    {
        "quaterId": "Q3-2023-bIDQzxZp04C",
        "budgetId": "bIDQzxZp04C",
        "name": "Q3 2023 - Education Transformation",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30"
    },
    {
        "quaterId": "Q4-2023-bIDQzxZp04C",
        "budgetId": "bIDQzxZp04C",
        "name": "Q4 2023 - Education Transformation",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31"
    }
]
disbursements = [
    # ==================== INFRASTRUCTURE (bIDEyNOJYTT) ====================
    {
        "budgetId": "bIDEyNOJYTT",
        "quaterId": "Q1-2023-bIDEyNOJYTT",
        "disbursementDate": "2023-03-10",
        "amountReleased": 1_200_000_000,
        "paymentMethod": "Bank Transfer",
        "disbursementOfficer": "Eng. Robert M. (FIN-WORKS-001)",
        "department": "Works and Transport",
        "status": "Completed",
        "evidence": "VOUCHER-WORKS-Q1-2023.pdf",
        "others": {
            "purpose": "Road construction and bridge rehabilitation",
            "bankRef": "BNK-WORKS-0323",
            "itemsCovered": ["Road Construction", "Bridge Rehabilitation", "Engineering Surveys"],
            "supplier": "National Construction Authority"
        }
    },
    {
        "budgetId": "bIDEyNOJYTT",
        "quaterId": "Q2-2023-bIDEyNOJYTT",
        "disbursementDate": "2023-06-15",
        "amountReleased": 950_000_000,
        "paymentMethod": "Bank Transfer",
        "disbursementOfficer": "Eng. Robert M. (FIN-WORKS-001)",
        "department": "Works and Transport",
        "status": "Completed",
        "evidence": "VOUCHER-WORKS-Q2-2023.pdf",
        "others": {
            "purpose": "Railway expansion and urban transport projects",
            "bankRef": "BNK-WORKS-0623",
            "itemsCovered": ["Railway Expansion", "Urban Light Rail", "Traffic Management Systems"],
            "supplier": "National Construction Authority"
        }
    },
    {
        "budgetId": "bIDEyNOJYTT",
        "quaterId": "Q3-2023-bIDEyNOJYTT",
        "disbursementDate": "2023-09-12",
        "amountReleased": 800_000_000,
        "paymentMethod": "Bank Transfer",
        "disbursementOfficer": "Eng. Robert M. (FIN-WORKS-001)",
        "department": "Works and Transport",
        "status": "Completed",
        "evidence": "VOUCHER-WORKS-Q3-2023.pdf",
        "others": {
            "purpose": "Rural connectivity and port infrastructure",
            "bankRef": "BNK-WORKS-0923",
            "itemsCovered": ["Rural Road Connectivity", "Port Dredging", "Public Transport Hubs"],
            "supplier": "National Construction Authority"
        }
    },
    {
        "budgetId": "bIDEyNOJYTT",
        "quaterId": "Q4-2023-bIDEyNOJYTT",
        "disbursementDate": "2023-12-05",
        "amountReleased": 650_000_000,
        "paymentMethod": "Bank Transfer",
        "disbursementOfficer": "Eng. Robert M. (FIN-WORKS-001)",
        "department": "Works and Transport",
        "status": "Completed",
        "evidence": "VOUCHER-WORKS-Q4-2023.pdf",
        "others": {
            "purpose": "Year-end infrastructure completion projects",
            "bankRef": "BNK-WORKS-1223",
            "itemsCovered": ["Drainage Systems", "Pedestrian Walkways", "Engineering Surveys"],
            "supplier": "National Construction Authority"
        }
    },

    # ==================== HEALTHCARE (bIDuIC1xEeG) ====================
    {
        "budgetId": "bIDuIC1xEeG",
        "quaterId": "Q1-2023-bIDuIC1xEeG",
        "disbursementDate": "2023-03-18",
        "amountReleased": 850_000_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "Dr. Sarah K. (FIN-HEALTH-001)",
        "department": "Health",
        "status": "Completed",
        "evidence": "VOUCHER-HEALTH-Q1-2023.pdf",
        "others": {
            "purpose": "Regional hospitals and vaccine procurement",
            "bankRef": "BNK-HEALTH-0323",
            "itemsCovered": ["Regional Hospitals", "Vaccine Procurement", "Medical Equipment"],
            "supplier": "National Medical Supplies Ltd"
        }
    },
    {
        "budgetId": "bIDuIC1xEeG",
        "quaterId": "Q2-2023-bIDuIC1xEeG",
        "disbursementDate": "2023-06-22",
        "amountReleased": 750_000_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "Dr. Sarah K. (FIN-HEALTH-001)",
        "department": "Health",
        "status": "Completed",
        "evidence": "VOUCHER-HEALTH-Q2-2023.pdf",
        "others": {
            "purpose": "HIV/AIDS programs and health worker training",
            "bankRef": "BNK-HEALTH-0623",
            "itemsCovered": ["HIV/AIDS Programs", "Health Worker Training", "Laboratory Reagents"],
            "supplier": "National Medical Supplies Ltd"
        }
    },
    {
        "budgetId": "bIDuIC1xEeG",
        "quaterId": "Q3-2023-bIDuIC1xEeG",
        "disbursementDate": "2023-09-15",
        "amountReleased": 700_000_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "Dr. Sarah K. (FIN-HEALTH-001)",
        "department": "Health",
        "status": "Completed",
        "evidence": "VOUCHER-HEALTH-Q3-2023.pdf",
        "others": {
            "purpose": "Malaria control and maternal health services",
            "bankRef": "BNK-HEALTH-0923",
            "itemsCovered": ["Malaria Control", "Maternal Health", "Surgical Supplies"],
            "supplier": "National Medical Supplies Ltd"
        }
    },
    {
        "budgetId": "bIDuIC1xEeG",
        "quaterId": "Q4-2023-bIDuIC1xEeG",
        "disbursementDate": "2023-12-08",
        "amountReleased": 600_000_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "Dr. Sarah K. (FIN-HEALTH-001)",
        "department": "Health",
        "status": "Completed",
        "evidence": "VOUCHER-HEALTH-Q4-2023.pdf",
        "others": {
            "purpose": "Ambulance fleet and mental health services",
            "bankRef": "BNK-HEALTH-1223",
            "itemsCovered": ["Ambulance Fleet", "Mental Health Services", "Health IT Systems"],
            "supplier": "National Medical Supplies Ltd"
        }
    },

    # ==================== EDUCATION (bIDQzxZp04C) ====================
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q1-2023-bIDQzxZp04C",
        "disbursementDate": "2023-03-12",
        "amountReleased": 700_000_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Prof. James L. (FIN-EDU-001)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q1-2023.pdf",
        "others": {
            "purpose": "Classroom construction and teacher recruitment",
            "bankRef": "BNK-EDU-0323",
            "itemsCovered": ["Classroom Construction", "Teacher Recruitment", "Textbook Provision"],
            "supplier": "National Education Services"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q2-2023-bIDQzxZp04C",
        "disbursementDate": "2023-06-18",
        "amountReleased": 650_000_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Prof. James L. (FIN-EDU-001)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q2-2023.pdf",
        "others": {
            "purpose": "STEM equipment and vocational training",
            "bankRef": "BNK-EDU-0623",
            "itemsCovered": ["STEM Equipment", "Vocational Training", "Science Labs"],
            "supplier": "National Education Services"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q3-2023-bIDQzxZp04C",
        "disbursementDate": "2023-09-20",
        "amountReleased": 600_000_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Prof. James L. (FIN-EDU-001)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q3-2023.pdf",
        "others": {
            "purpose": "Digital learning and special needs education",
            "bankRef": "BNK-EDU-0923",
            "itemsCovered": ["Digital Learning", "Special Needs Education", "Sports Facilities"],
            "supplier": "National Education Services"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q4-2023-bIDQzxZp04C",
        "disbursementDate": "2023-12-10",
        "amountReleased": 500_000_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Prof. James L. (FIN-EDU-001)",
        "department": "Education",
        "status": "Completed",
        "evidence": "VOUCHER-EDU-Q4-2023.pdf",
        "others": {
            "purpose": "Teacher housing and university research grants",
            "bankRef": "BNK-EDU-1223",
            "itemsCovered": ["Teacher Housing", "University Research Grants", "School Feeding"],
            "supplier": "National Education Services"
        }
    }
]
education_expenditures = [
    # Q1
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q1-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-03-18",
        "amountSpent": 650_000_000,
        "beneficially": "School Construction Unit",
        "description": "New classroom construction",
        "evidence": "EXP-EDU-Q1-001",
        "detailsOfExpense": {
            "items": ["Cement", "Roofing Sheets", "Windows"],
            "quantity": [10000, 5000, 2000],
            "amount": [15000, 25000, 12000],
            "categories": ["Infrastructure", "Infrastructure", "Infrastructure"],
            "supplier": "National Builders Ltd",
            "evidence": "EXP-EDU-Q1-001"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q1-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-03-29",
        "amountSpent": 600_000_000,
        "beneficially": "Teacher Service Commission",
        "description": "Teacher recruitment drive",
        "evidence": "EXP-EDU-Q1-002",
        "detailsOfExpense": {
            "items": ["Teacher Salaries", "Training Workshops"],
            "quantity": [500, 25],
            "amount": [1000000, 4000000],
            "categories": ["Human Resources", "Human Resources"],
            "supplier": "Teacher Service Commission",
            "evidence": "EXP-EDU-Q1-002"
        }
    },

    # Q2
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q2-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-06-12",
        "amountSpent": 620_000_000,
        "beneficially": "STEM Education Initiative",
        "description": "Science lab equipment",
        "evidence": "EXP-EDU-Q2-001",
        "detailsOfExpense": {
            "items": ["Microscopes", "Chemistry Sets"],
            "quantity": [500, 800],
            "amount": [120000, 350000],
            "categories": ["STEM Education", "STEM Education"],
            "supplier": "Science Equipment Ltd",
            "evidence": "EXP-EDU-Q2-001"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q2-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-06-28",
        "amountSpent": 580_000_000,
        "beneficially": "Vocational Training Board",
        "description": "Technical skills equipment",
        "evidence": "EXP-EDU-Q2-002",
        "detailsOfExpense": {
            "items": ["Welding Machines", "Carpentry Tools"],
            "quantity": [120, 250],
            "amount": [2500000, 1000000],
            "categories": ["Skills Development", "Skills Development"],
            "supplier": "Technical Skills Ltd",
            "evidence": "EXP-EDU-Q2-002"
        }
    },

    # Q3
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q3-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-09-15",
        "amountSpent": 550_000_000,
        "beneficially": "Digital Learning Program",
        "description": "ICT equipment for schools",
        "evidence": "EXP-EDU-Q3-001",
        "detailsOfExpense": {
            "items": ["Laptops", "Projectors"],
            "quantity": [5000, 1200],
            "amount": [80000, 25000],
            "categories": ["ICT in Education", "ICT in Education"],
            "supplier": "Digital Learning Solutions",
            "evidence": "EXP-EDU-Q3-001"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q3-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-09-30",
        "amountSpent": 500_000_000,
        "beneficially": "Special Needs Education",
        "description": "Inclusive education materials",
        "evidence": "EXP-EDU-Q3-002",
        "detailsOfExpense": {
            "items": ["Braille Printers", "Hearing Aids"],
            "quantity": [50, 500],
            "amount": [5000000, 500000],
            "categories": ["Inclusive Education", "Inclusive Education"],
            "supplier": "Accessible Learning Ltd",
            "evidence": "EXP-EDU-Q3-002"
        }
    },

    # Q4
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q4-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-12-15",
        "amountSpent": 480_000_000,
        "beneficially": "University Grants Committee",
        "description": "Research funding",
        "evidence": "EXP-EDU-Q4-001",
        "detailsOfExpense": {
            "items": ["Lab Equipment", "Research Stipends"],
            "quantity": [45, 120],
            "amount": [6000000, 1500000],
            "categories": ["Research Development", "Research Development"],
            "supplier": "National Research Council",
            "evidence": "EXP-EDU-Q4-001"
        }
    },
    {
        "budgetId": "bIDQzxZp04C",
        "quaterId": "Q4-2023-bIDQzxZp04C",
        "dateOfExpense": "2023-12-28",
        "amountSpent": 450_000_000,
        "beneficially": "School Feeding Program",
        "description": "Nutrition supplies",
        "evidence": "EXP-EDU-Q4-002",
        "detailsOfExpense": {
            "items": ["Fortified Meals", "Milk Packets"],
            "quantity": [3000000, 5000000],
            "amount": [100, 30],
            "categories": ["Nutrition", "Nutrition"],
            "supplier": "National Food Suppliers",
            "evidence": "EXP-EDU-Q4-002"
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
    # for quater in education_expenditures:
    #     print(db.insertDataIntoExpenditure(quater))

# my stress test is on these bIDEyNOJYTT,bIDuIC1xEeG,bIDQzxZp04C
    # pprint.pprint(db.getExpendituresByBudgetQuarter("bIDvWU6mkod","qId7MFFvF"))
    # pprint.pprint(db.getQuartersByBudgetId('bIDvWU6mkod'))
    
    # pprint.pprint(db.getAnyTableData({
    #     'tableName': 'expenditure',
    #     'columns': ['*'],
    #     'condition': 'budgetId = ?',
    #     'conditionalData': ['bIDc99CtOVM'],
    #     'limit':4,
    #     'returnDicts': True,
    #     'returnNamespaces': False,
    #     'parseJson': True,
    #     'returnGenerator': False 
        
    # })    )
    # metrics = utils.getQuarterlyPerfromanceMetric('bIDc99CtOVM')
    # pprint.pprint(metrics)
    # plot_quarterly_pies_detailed('bIDvWU6mkod','/workspaces/budgetMornitoringSystem/budgetMonitoring/database')
    # pprint.pprint(metrics)
    # print(plot_quarterly_activities(metrics,save_path='quarterly_performance.png'))
    pprint.pprint(utils.getQuarterlyPerfromanceMetric('bIDc99CtOVM'))
    # pprint.pprint(utils.getExpendituresByBudgetQuarterDate('bIDvWU6mkod','qId7MFFvF','2023-12'))
        # pass
        
        
      