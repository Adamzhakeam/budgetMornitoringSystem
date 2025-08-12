import db
import utils
import pprint
quarters_data = [
    # Quarters for Health Budget (bIDziMnNLhw)
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q1-2023",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31",
        "others": {
            "plannedRelease": 1_200_000,
            "actualRelease": 1_200_000,
            "approvalStatus": "fully_released"
        }
    },
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q2-2023",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30",
        "others": {
            "plannedRelease": 1_200_000,
            "actualRelease": 800_000,
            "approvalStatus": "partial_released",
            "notes": "Delayed due to revenue shortfall"
        }
    },
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q3-2023",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30",
        "others": {
            "plannedRelease": 1_200_000,
            "actualRelease": 700_000,
            "approvalStatus": "partial_released"
        }
    },
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q4-2023",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31",
        "others": {
            "plannedRelease": 1_400_000,
            "actualRelease": 500_000,
            "approvalStatus": "under_review",
            "notes": "Pending parliamentary approval for supplementary budget"
        }
    },

    # Quarters for Education Budget (bIDZk6NDMbf)
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q1-2023",
        "startDate": "2023-01-01",
        "endDate": "2023-03-31",
        "others": {
            "plannedRelease": 900_000,
            "actualRelease": 900_000,
            "approvalStatus": "fully_released"
        }
    },
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q2-2023",
        "startDate": "2023-04-01",
        "endDate": "2023-06-30",
        "others": {
            "plannedRelease": 900_000,
            "actualRelease": 600_000,
            "approvalStatus": "partial_released",
            "notes": "Prioritized exam materials first"
        }
    },
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q3-2023",
        "startDate": "2023-07-01",
        "endDate": "2023-09-30",
        "others": {
            "plannedRelease": 800_000,
            "actualRelease": 400_000,
            "approvalStatus": "partial_released"
        }
    },
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q4-2023",
        "startDate": "2023-10-01",
        "endDate": "2023-12-31",
        "others": {
            "plannedRelease": 400_000,
            "actualRelease": 200_000,
            "approvalStatus": "pending",
            "notes": "Year-end budget freeze"
        }
    }
]

disbursements = [
    # ================= HEALTH BUDGET (bIDziMnNLhw) =================
    # Q1 Release (Full)
    {
        "budgetId": "bIDziMnNLhw",
        "disbursementDate": "2023-03-15",
        "amountReleased": 1_200_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "James M. (FIN-2023)",
        "department": "Health",
        "status": "Completed",
        "evidence": "voucher_health_Q1_2023.pdf",
        "others": {
            "quarter": "Q1-2023",
            "purpose": "Essential medicines procurement",
            "bankRef": "BNK-HEALTH-0323"
        }
    },
    # Q2 Release (Partial)
    {
        "budgetId": "bIDziMnNLhw",
        "disbursementDate": "2023-06-20",
        "amountReleased": 800_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Sarah K. (FIN-2023)",
        "department": "Health",
        "status": "Completed",
        "evidence": "voucher_health_Q2_2023.pdf",
        "others": {
            "quarter": "Q2-2023",
            "purpose": "Hospital equipment maintenance",
            "chequeNo": "CHQ-456789",
            "notes": "Reduced due to revenue shortfall"
        }
    },
    # Q3 Release (Partial)
    {
        "budgetId": "bIDziMnNLhw",
        "disbursementDate": "2023-09-10",
        "amountReleased": 700_000,
        "paymentMethod": "Wire Transfer",
        "disbursementOfficer": "James M. (FIN-2023)",
        "department": "Health",
        "status": "Completed",
        "evidence": "voucher_health_Q3_2023.pdf",
        "others": {
            "quarter": "Q3-2023",
            "purpose": "Staff salaries and incentives",
            "swiftCode": "UGANDA-HEALTH"
        }
    },
    # Q4 Release (Under Review)
    {
        "budgetId": "bIDziMnNLhw",
        "disbursementDate": "2023-12-05",
        "amountReleased": 500_000,
        "paymentMethod": "Mobile Money",
        "disbursementOfficer": "Sarah K. (FIN-2023)",
        "department": "Health",
        "status": "Pending",
        "evidence": "voucher_health_Q4_2023.pdf",
        "others": {
            "quarter": "Q4-2023",
            "purpose": "Emergency COVID supplies",
            "mobileRef": "MM-123456",
            "notes": "Partial release pending supplementary budget"
        }
    },

    # ================= EDUCATION BUDGET (bIDZk6NDMbf) =================
    # Q1 Release (Full)
    {
        "budgetId": "bIDZk6NDMbf",
        "disbursementDate": "2023-03-10",
        "amountReleased": 900_000,
        "paymentMethod": "EFT",
        "disbursementOfficer": "David L. (FIN-2023)",
        "department": "Education",
        "status": "Completed",
        "evidence": "voucher_edu_Q1_2023.pdf",
        "others": {
            "quarter": "Q1-2023",
            "purpose": "Textbook printing and distribution",
            "bankRef": "BNK-EDU-0323"
        }
    },
    # Q2 Release (Partial)
    {
        "budgetId": "bIDZk6NDMbf",
        "disbursementDate": "2023-06-15",
        "amountReleased": 600_000,
        "paymentMethod": "Cheque",
        "disbursementOfficer": "Grace N. (FIN-2023)",
        "department": "Education",
        "status": "Completed",
        "evidence": "voucher_edu_Q2_2023.pdf",
        "others": {
            "quarter": "Q2-2023",
            "purpose": "Science lab kits for 200 schools",
            "chequeNo": "CHQ-987654",
            "notes": "Prioritized exam materials"
        }
    },
    # Q3 Release (Partial)
    {
        "budgetId": "bIDZk6NDMbf",
        "disbursementDate": "2023-09-05",
        "amountReleased": 400_000,
        "paymentMethod": "Wire Transfer",
        "disbursementOfficer": "David L. (FIN-2023)",
        "department": "Education",
        "status": "Completed",
        "evidence": "voucher_edu_Q3_2023.pdf",
        "others": {
            "quarter": "Q3-2023",
            "purpose": "Teacher training workshops",
            "swiftCode": "UGANDA-EDU"
        }
    },
    # Q4 Release (Pending)
    {
        "budgetId": "bIDZk6NDMbf",
        "disbursementDate": "2023-12-01",
        "amountReleased": 200_000,
        "paymentMethod": "Mobile Money",
        "disbursementOfficer": "Grace N. (FIN-2023)",
        "department": "Education",
        "status": "Pending",
        "evidence": "voucher_edu_Q4_2023.pdf",
        "others": {
            "quarter": "Q4-2023",
            "purpose": "School maintenance grants",
            "mobileRef": "MM-654321",
            "notes": "Year-end budget freeze affected release"
        }
    }
    
]

expenditures = [
    # ================= HEALTH BUDGET (bIDziMnNLhw) =================
    # Q1 Expenditure (1.2M disbursed)
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q1-2023",
        "dateOfExpense": "2023-03-20",
        "amountSpent": 1_200_000,
        "detailsOfExpense": {
            "items": ["COVID Vaccines", "Antibiotics", "Medical Gloves"],
            "quantity": [80_000, 50_000, 200_000],
            "amount": [10, 8, 0.5],  # Unit prices
            "categories": ["Vaccines", "Medicines", "PPE"]
        },
        "beneficially": "National Referral Hospital",
        "description": "Q1 Essential Medical Supplies",
        "evidence": "INV-MED-Q1-2023.pdf",
        "others": {
            "disbursementRef": "dIDq1Health",  # Link to Q1 disbursement
            "procurementMethod": "Open Tender"
        }
    },
    # Q2 Expenditure (800K disbursed)
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q2-2023",
        "dateOfExpense": "2023-06-25",
        "amountSpent": 800_000,
        "detailsOfExpense": {
            "items": ["X-Ray Machine", "Ultrasound Device"],
            "quantity": [2, 3],
            "amount": [300_000, 200_000],  # Bulk unit prices
            "categories": ["Equipment", "Equipment"]
        },
        "beneficially": "Regional Hospitals",
        "description": "Q2 Medical Equipment Upgrade",
        "evidence": "INV-EQUIP-Q2-2023.pdf",
        "others": {
            "disbursementRef": "dIDq2Health",
            "supplier": "MediTech Solutions"
        }
    },
    # Q3 Expenditure (700K disbursed)
    {
        "budgetId": "bIDziMnNLhw",
        "quaterId": "Q3-2023",
        "dateOfExpense": "2023-09-15",
        "amountSpent": 700_000,
        "detailsOfExpense": {
            "items": ["Doctor Salaries", "Nurse Salaries"],
            "quantity": [15, 40],  # Staff counts
            "amount": [30_000, 10_000],  # Monthly salaries
            "categories": ["Salaries", "Salaries"]
        },
        "beneficially": "Health Ministry Staff",
        "description": "Q3 Personnel Costs",
        "evidence": "PAYROLL-Q3-2023.pdf",
        "others": {
            "disbursementRef": "dIDq3Health",
            "payPeriod": "July-Sept 2023"
        }
    },

    # ================= EDUCATION BUDGET (bIDZk6NDMbf) =================
    # Q1 Expenditure (900K disbursed)
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q1-2023",
        "dateOfExpense": "2023-03-18",
        "amountSpent": 900_000,
        "detailsOfExpense": {
            "items": ["Math Textbooks", "Science Kits"],
            "quantity": [60_000, 1_000],
            "amount": [10, 300],  # Unit prices
            "categories": ["Books", "Lab Equipment"]
        },
        "beneficially": "Public Secondary Schools",
        "description": "Q1 Learning Materials",
        "evidence": "INV-EDU-Q1-2023.pdf",
        "others": {
            "disbursementRef": "dIDq1Edu",
            "distributionList": "SCHOOLS-2023.xlsx"
        }
    },
    # Q2 Expenditure (600K disbursed)
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q2-2023",
        "dateOfExpense": "2023-06-20",
        "amountSpent": 600_000,
        "detailsOfExpense": {
            "items": ["Desks", "Chairs"],
            "quantity": [2_000, 2_000],
            "amount": [200, 100],  # Unit prices
            "categories": ["Furniture", "Furniture"]
        },
        "beneficially": "Rural Schools",
        "description": "Q2 Classroom Furniture",
        "evidence": "INV-FURN-Q2-2023.pdf",
        "others": {
            "disbursementRef": "dIDq2Edu",
            "deliveryStatus": "Completed"
        }
    },
    # Q3 Expenditure (400K disbursed)
    {
        "budgetId": "bIDZk6NDMbf",
        "quaterId": "Q3-2023",
        "dateOfExpense": "2023-09-10",
        "amountSpent": 400_000,
        "detailsOfExpense": {
            "items": ["Teacher Training", "Workshop Materials"],
            "quantity": [200, 1],  # 200 teachers
            "amount": [1_800, 40_000],  # Training cost per teacher + materials
            "categories": ["Training", "Materials"]
        },
        "beneficially": "National Teachers",
        "description": "Q3 Capacity Building",
        "evidence": "INV-TRAIN-Q3-2023.pdf",
        "others": {
            "disbursementRef": "dIDq3Edu",
            "venue": "Kampala Institute"
        }
    }
]
if __name__ == "__main__":
    
    # for quater in expenditures:
    #     print(db.insertDataIntoExpenditure(quater))
    # pprint.pprint(db.getExpendituresByBudgetQuarter("bIDziMnNLhw","qIdWoekU3"))
    # pprint.pprint(db.getQuartersByBudgetId('bIDziMnNLhw'))
    
    def budgetQuaterPerformance(budgetId:str):
        qd = db.getQuartersByBudgetId(budgetId)['data']
        quaters = [],proposedAmount = 0,workingAmount = 0
        for index in range(len(qd)):
            quaters.append(qd[index]['quaterId'])
        for index in range(len(quaters)):
            pass
    print(budgetQuaterPerformance('bIDziMnNLhw'))
        