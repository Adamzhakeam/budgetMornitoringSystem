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
    
    :param `expenseDetails`: date of the expense as a string (e.g., '2025-08-11')
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
    'condition': '',  # Add filters
    'conditionalData': [],
    'limit': 100,                  # Limit results
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