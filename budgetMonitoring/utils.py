'''
    this file contains functions required for plotting performance and making various 
    calculations to aquire performance amounts and percntages 
'''
from datetime import datetime
import pandas as pd
import db

def getOverallPercentages(budgetAmount:dict,expenditureAmount:dict)->dict:
    '''
    this module is responsible for calculating overall percentages and amount of remaining
    balance after all exepenses are deducted 
    
    @ param `budgetAmount`:  is a dictionary that expects a key `workingAmount`
    @ param `expenditureamount`:  is a dictionary thats expects a key `totalExpenses`
    '''
    remainingAmount = budgetAmount['workingAmount'] - expenditureAmount['totalExpenses']
    remainingPercentage = (remainingAmount/budgetAmount['workingAmount'])*100
    expenditurePercentage = (expenditureAmount['totalExpenses']/budgetAmount['workingAmount'])*100
    return{'expenditurePercentage':expenditurePercentage,'remainingAmount':remainingAmount,
                   'remainingPercentage':remainingPercentage}
    
def getExpenditureTotals(expenseDetails:dict)->dict:
    '''
        this module is responsible for calculating the overall total amount spent and then 
        also it calculates the total amount of money spent per item 
        
        @ param `expenseDetails`:  is a dictionary that expects `quantity`,`items`,`amount` as keys 
                    whose values are lists
    '''
    itemTotals = {}
    itemTotalsList = []
    overallTotal = 0
    for index in range(len(expenseDetails['items'])):
        itemTotals.update({expenseDetails['items'][index]:
            expenseDetails['quantity'][index]*expenseDetails['amount'][index]})
        itemTotalsList.append(expenseDetails['quantity'][index]*expenseDetails['amount'][index])
        overallTotal+=itemTotalsList[index]
    return{'overallTotal':overallTotal,'itemTotals':itemTotals}

def getItemExpendutureBehaviour(proposedItemDetails:dict,actualItemDetails:dict)->dict:
    '''
    this function is responsible for calulating the behavial expenditure of various items 
    on the budget against the planned 
    
    @ param `proposedItemDetails`:  is a dictionary that expects `itemTotals` as key and proposed/planned item 
                details originate from proposed/planned budget
                
    @ param `actualItemDetails`:  is a dictionary that expects `itemTotals` as key and actualItemDetails originate from the 
                the working budget and current quater  
    '''
    evaluatedData = {}
    for item,amount in proposedItemDetails['itemTotals'].items():
        # print(actualItemDetails['itemTotals'][item])
        evaluatedData.update({item:amount-actualItemDetails['itemTotals'][item]})
    expenditurePercentages = getOverallPercentages({'workingAmount':proposedItemDetails['overallTotal']},
                                                    {'totalExpenses':actualItemDetails['overallTotal']})
    return{'evaluatedData':evaluatedData,'expenditurePercentages':expenditurePercentages}

def quarterIdForExpense(expenseDetails: dict) -> dict:
    """
    Given a date string in 'YYYY-MM-DD' format and a list of quarter ranges,
    returns the quarterId for that date.
    
    :param `expenseDetails`: `dateOfExpense` as a string (e.g., '2025-08-11') and `budgetId` as a string too
    :param `quarterRanges`: List of dicts with 'quarterId', 'startDate', and 'endDate'
                          Example:
                          [
                              {'quarterId': 1, 'startDate': '2025-01-01', 'endDate': '2025-03-31'}
                          ]
    :return: quarterId (str) in a dictionary
    """
    query_all_quarters = {
    'tableName': 'budgetQuaters',  # Required
    'columns': ['*'],             # Fetch all columns
    'returnDicts': True,          # Return as dictionaries
    'parseJson': True,            # Parse JSON fields
    'condition': 'budgetId = ?',  # Add filters
    'conditionalData': [expenseDetails['budgetId']],
    'limit': 4,                  # Limit results
    'returnNamespaces': False,    # Alternative to dicts
    'returnGenerator': True    # For large datasets
}
    quarterRanges = db.getAnyTableData(query_all_quarters)['data']
    expenseDate = datetime.strptime(expenseDetails['dateOfExpense'], "%Y-%m-%d")

    for quarter in quarterRanges:
        start = datetime.strptime(quarter['startDate'], "%Y-%m-%d")
        end = datetime.strptime(quarter['endDate'], "%Y-%m-%d")

        if start <= expenseDate <= end:
            return {'status':True,'log':"", 'data':{'quaterId':quarter['quaterId']}}

    return {'status':False,'log':'date not in any quater range'}

def getQuarterlyPerfromanceMetric(budgetId: str) -> dict:
    """
    Returns performance metrics with category-based analysis and item-level details:
    {
        "Q1-2023": {
            "financial": { ... },  # Same as before
            "category_analysis": {
                "Materials": {
                    "planned": float,
                    "actual": float,
                    "variance": float,
                    "items": {
                        "Textbooks": {"actual": 500000, "variance": -20000},
                        "Notebooks": {"actual": 300000, "variance": +50000}
                    }
                },
                ...
            },
            "budget_health": { ... }  # Same as before
        },
        ...
    }
    """
    # Get all quarters
    quarters_res = db.getQuartersByBudgetId(budgetId)
    if not quarters_res['status']:
        return {"error": quarters_res['log']}
    
    # Get planned items and categories from original budget
    budget = db.getPalnnedByBudgetId(budgetId)
    if not budget.get('status'):
        return {"error": "Budget not found"}
    
    planned_items, planned_categories = extractPlaanedData(budget['data'][0])
    
    # Process each quarter
    results = {}
    for quarter in quarters_res['data']:
        quarter_id = quarter['quaterId']
        
        # Get financial data
        disbursements = getDisbursementsForQuarter(budgetId, quarter_id)
        expenditures = getExpendituresForQuarter(budgetId, quarter_id)
        
        # Calculate metrics
        results[quarter_id] = {
            "financial": calculateFinancialMetrics(
                planned=sum(planned_items.values()),
                disbursed=disbursements['total'],
                expended=expenditures['total'],
                items=expenditures['items']
            ),
            "category_analysis": calculateCategoryPerformance(
                planned_items,
                planned_categories,
                expenditures['item_details']
            ),
            "budget_health": calculateUtilisation(
                disbursements['total'],
                expenditures['total']
            )
        }
    
    return results

# New Helper Functions
def getDisbursementsForQuarter(budgetId: str, quarterId: str) -> dict:
    """Returns {'total': float, 'transactions': list}"""
    res = db.getDisbursementsByBudgetQuarter(budgetId, quarterId)
    if not res['status']:
        return {'total': 0.0, 'transactions': []}
    return {
        'total': sum(t['amountReleased'] for t in res['data']),
        'transactions': res['data']
    }
    
def calculateFinancialMetrics(planned: float, disbursed: float, 
                              expended: float, items: list) -> dict:
    """Calculates variance and standard deviation"""
    return {
        "planned": planned,
        "disbursed": disbursed,
        "expended": expended,
        "variance": disbursed - expended,
        "std_dev": None #pd.Series(items).std() if len(items) > 1 else 0.0
    }

def calculateUtilisation(disbursed: float, expended: float) -> dict:
    """Calculates budget utilization percentages"""
    return {
        "utilization_percentage": (expended / disbursed * 100) if disbursed else 0.0,
        "remaining_amount": disbursed - expended
    }
    
def extractPlaanedData(budget: dict) -> tuple:
    """Extracts planned items and their categories"""
    details = budget['detailsOfBudget']
    planned_items = {}
    planned_categories = {}
    
    for i in range(len(details['items'])):
        item = details['items'][i]
        planned_items[item] = details['quantity'][i] * details['amount'][i]
        planned_categories[item] = details['categories'][i]
    
    return planned_items, planned_categories

def getExpendituresForQuarter(budgetId: str, quarterId: str) -> dict:
    """Enhanced to return category and item details"""
    res = db.getExpendituresByBudgetQuarter(budgetId, quarterId)
    if not res['status']:
        return {'total': 0.0, 'items': [], 'item_details': {}}
    
    all_amounts = []
    item_details = {}
    
    for record in res['data']:
        details = record['detailsOfexpense']
        for i in range(len(details['items'])):
            item = details['items'][i]
            amount = details['quantity'][i] * details['amount'][i]
            category = details['categories'][i]
            
            all_amounts.append(amount)
            
            # Structure: {item: {amount, category, ...}}
            item_details[item] = {
                'amount': amount,
                'category': category,
                'quantity': details['quantity'][i],
                'unit_price': details['amount'][i]
            }
    
    return {
        'total': sum(all_amounts),
        'items': all_amounts,
        'item_details': item_details
    }

def calculateCategoryPerformance(planned_items: dict, 
                                 planned_categories: dict,
                                 actual_items: dict) -> dict:
    """Calculates performance by category with item-level breakdown"""
    category_metrics = {}
    
    # Initialize categories from planned budget
    for item, category in planned_categories.items():
        if category not in category_metrics:
            category_metrics[category] = {
                'planned': 0.0,
                'actual': 0.0,
                'items': {}
            }
        category_metrics[category]['planned'] += planned_items.get(item, 0.0)
    
    # Add actual expenditures
    for item, details in actual_items.items():
        category = details['category']
        amount = details['amount']
        
        # Initialize category if not in original plan
        if category not in category_metrics:
            category_metrics[category] = {
                'planned': 0.0,
                'actual': 0.0,
                'items': {}
            }
        
        category_metrics[category]['actual'] += amount
        category_metrics[category]['items'][item] = {
            'actual': amount,
            'variance': (planned_items.get(item, 0) - amount)
        }
    
    # Calculate category variances
    for category, data in category_metrics.items():
        data['variance'] = data['planned'] - data['actual']
    
    return category_metrics


