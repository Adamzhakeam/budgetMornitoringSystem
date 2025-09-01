'''
hey this is a testing module     
'''

import db
import chartsOfAccounts
import utils
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import os
from Levenshtein import distance as levenshtein_distance

   

quarters = [
    # Budget 1: bIDEyNOJYTT (Infrastructure)
    {
        "quaterId": "Q1-2023-bIDEyNOJYTT",
        "budgetId": "bIDEyNOJYTT",
        "name": "Q1 2023 - National Infrastructure",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31"
    },
    
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
    
]
budgets = [
    {
        # Health Ministry Budget (FY 2023)
        "dateOfApproval": "2025-01-10",
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
    
]










if __name__ == "__main__":
    
    # pprint.pprint(budgetQuaterPerformance("bIDziMnNLhw"))
    # for quater in education_expenditures:
    #     print(db.insertDataIntoExpenditure(quater))

# my stress test is on these bIDEyNOJYTT,bIDuIC1xEeG,bIDQzxZp04C
    # pprint.pprint(db.getExpendituresByBudgetQuarter("bIDvWU6mkod","qId7MFFvF"))
    # pprint.pprint(db.getQuartersByBudgetId('bIDvWU6mkod'))
    
    pprint.pprint(db.getAnyTableData({
        'tableName': 'budget',
        'columns': ['*'],
        'condition': 'budgetId = ?',
        'conditionalData': ['bIDEyNOJYTT'],
        'limit':100,
        'returnDicts': True,
        'returnNamespaces': False,
        'parseJson': True,
        'returnGenerator': False 
        
    })    )
    # metrics = utils.getQuarterlyPerfromanceMetric('bIDc99CtOVM')
    # pprint.pprint(metrics)
    # plot_quarterly_pies_detailed('bIDvWU6mkod','/workspaces/budgetMornitoringSystem/budgetMonitoring/database')
    # pprint.pprint(metrics)
    # print(plot_quarterly_activities(metrics,save_path='quarterly_performance.png'))
    # pprint.pprint(utils.getQuarterlyPerfromanceMetric('bIDziMnNLhw'))
    # pprint.pprint(utils.getExpendituresByBudgetQuarterDate('bIDvWU6mkod','qId7MFFvF','2023-12'))
    # pprint.pprint(db.getAnyChartAccount('israel'))
        # pass
        
        
      