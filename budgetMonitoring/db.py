'''
    the modules are resposible for handling database logic insert,
    read,delete,select and update  data into the database 
    
    the modules below will consiste of functions and classes 
'''

import kisa_utils as kutils
import chartsOfAccounts
import utils


def createTables():
    '''
        this function is responsible for creating the database tables 
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTables = kutils.config.getValue('bbmsDb/tables')
    
    with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
        creationResponse = db.createTables(dbTables)
        print('>>>>>>>>>>>>>>tables didnt exist')
    return creationResponse

# --- the modules below are all responsible for handling tables for the charts of accounts 

def makeDataInserter():
    def insertDataIntoDb(tableName:str, data:dict):
        try:
            dbPath = kutils.config.getValue('bbmsDb/dbPath')
            dbTables = kutils.config.getValue('bbmsDb/tables')
            
            with kutils.db.Api(dbPath, dbTables, readonly=False) as db:
                for code, description in data.items():
                    response = db.insert(tableName, [code, description])
                return response
        except Exception as e:
            return {'status': False, 'error': str(e)}
    
    return insertDataIntoDb


# --#-- the modules below are responsible for handling users----- #---#--#--#-

def createuser(userDetails:dict)->dict:
    '''
        this module is responsible for creation of a user 
        @param userDetails:'userName','password',
                            'phoneNumber','roleId','email' are the expected keys 
        returns a dictionary with status and log 
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    passwordHash = kutils.encryption.hash(userDetails['password'])
    entryId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    userId = kutils.codes.new()
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        phoneNumberResponse = db.fetch(
            'users',
            ['phoneNumber'],
            'phoneNumber = ?',
            [userDetails['phoneNumber']],
            limit = 1,
            returnDicts=True,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        if len(phoneNumberResponse) > 0:
            return{'status':False, 'log':'phoneNumber already exists attached to another user please try another'}
        userCreationResponse = db.insert(
            'users',
            [entryId,timestamp,userId,userDetails['userName'],
             passwordHash,userDetails['phoneNumber'],userDetails['email'],userDetails['roleId']]
        )
    return(userCreationResponse)

def fetchAllusers()->list:
    '''
        this function is responsible for fetching customer from db
        by use of phone number
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        customerFetchResponse = db.fetch(
            'users',
            ['*'],
            '',
            [],limit = 100,
            returnDicts= True,returnNamespaces=False,parseJson=False,returnGenerator=False
        )
        if len(customerFetchResponse) == 0:
            return {
                'status':False,
                'log':'you havent registered any users yet'
            }
        return {
            'status':True,
            'log':customerFetchResponse
        }
def fetchuserByPhoneNumber(userDetails:dict)->dict:
    '''
    this module is responsible for fetching user by phone number
    @param userDetails:expected keys 'phoneNumber'
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    
    with kutils.db.Api(dbPath, dbTable, readonly=True) as db:
        userFetchResponse = db.fetch(
            'users',['*'],'phoneNumber=?',[userDetails['phoneNumber']],
            limit = 1 ,returnDicts= True,
            returnNamespaces=False,parseJson=False,returnGenerator=False
        )  
        if  len(userFetchResponse) == 0 :
            return {
                'status':False,
                'log':f'No users found registered under {userDetails["phoneNumber"]}'
            } 
        return{
            'status':True,
            'log':userFetchResponse
        }

def insertRevokeduser(userDetails:dict) -> dict:
    '''
        this module is responsible for inserting a revoked user into db 
        @param userDetails:entryId, timestamp, userId,userName,password ,phoneNumber, email,roleId,other the following 
                            are the expected keys
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    with kutils.db.Api(dbPath, dbTable, readonly = False) as db:
        entryId = kutils.codes.new()
        timestamp = kutils.dates.currentTimestamp()
        if userDetails['other']['revokerId'] == userDetails['userId']:
            return{
                'status':False,
                'log':'user can`t revoke themselves'
            }
        revokeduserInsertionResponse = db.insert( 'revokeduser',
                                                 [entryId,timestamp,userDetails['userId'],userDetails['userName'],
                                                      userDetails['password'],userDetails['phoneNumber'],userDetails['email'],
                                                      userDetails['roleId'],userDetails['other']])
        return revokeduserInsertionResponse   
    
def resetuserPassword(userDetails:dict)->dict:
    '''
        this function is responsible for resetting users password
        @param userDetails: 'phoneNumber' is the expected key  
    ''' 
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    newPassword = kutils.codes.new(8)
    passwordHash = kutils.encryption.hash(newPassword)
    if fetchuserByPhoneNumber({'phoneNumber':userDetails['phoneNumber']})['status']:
        email = fetchuserByPhoneNumber({'phoneNumber':userDetails['phoneNumber']})['log'][0]['email']
        with kutils.db.Api(dbPath,dbTable,readonly=False) as db:
            passwordUpdateResponse = db.update('users',
                                               ['password'],[passwordHash],'phoneNumber = ?',
                                               [userDetails['phoneNumber']])
            if passwordUpdateResponse['status']:
                return{'status':True,'log':f"your new password is: {newPassword}",'email':email}
            return passwordUpdateResponse
    return {'status':False,'log':'There is no user registered under the phoneNumber provided '}

# -- this module responsible for creating roles 
def createRoles(roleDetails:dict)->dict:
    '''
        this module is responsible for creation of roles and adding them to the db
        @param roleDetails:'entryId','timestamp','roleId','role','others'
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    entryId = kutils.codes.new()
    roleId = kutils.codes.new()
    timestamp = kutils.dates.currentTimestamp()
    role = roleDetails['role'].upper()
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        roleInsertionResponse = db.insert(
            'roles',
            [entryId,timestamp,roleId,role,roleDetails['others']]
        )
        return roleInsertionResponse
    
def fetchRole(roleDetails:dict)->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'roles',
            ['role'],
            'roleId = ?',
            [roleDetails['roleId']],
            limit = 1,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"role does not exist"
            }
        
        return {
            'status':True,
            'log':roleFetchResults
        }
    
    
def fetchAllRoles()->list:
    '''
        this function is responsible for fetching the user role 
        from database 
        @param roleId:
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    dbTable = kutils.config.getValue('bbmsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        roleFetchResults = db.fetch(
            'roles',
            ['*'],
            '',
            [],
            limit = 100,
            returnDicts=True,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator= False
        )
        if len(roleFetchResults) == 0:
            return{
                'status':False,
                'log':"you haven`t registered any roles yet"
            }
        return{
            'status':True,
            'log':roleFetchResults
        }
        
# --the modules below are responsible for adding data into budget table 

def insertDataIntoBudget(budgetDetails:dict)->dict:
    '''
    this module is responsible for inserting data into the table budget
    
    @ param `budgetDetails` : is a dictionary with expected keys 
                                `department`,`vote`,`programme`,`working`,`planned`,
                                `dateOfApproval`,`detailsOfBudget`,`others`,`description`
                                
    @ return : function returns a dictionary with a `status` when `False` it has a log 
                when `True` means operation was successful
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    budgetId = 'bID'+kutils.codes.new(8)
    timestamp = kutils.dates.currentTimestamp()
    
    with kutils.db.Api(dbPath,tables,readonly=False) as db:
        insertionResponse = db.insert('budget',[budgetId,timestamp,budgetDetails['dateOfApproval'],
                                                budgetDetails['planned'],budgetDetails['working'],budgetDetails['department'],
                                                budgetDetails['programme'],budgetDetails['vote'],budgetDetails['detailsOfBudget'],
                                                budgetDetails['description'],budgetDetails.get('others',{})])
        return insertionResponse
    
def getAnyTableData(tableDetails:dict)-> dict:
    '''
        this function is responsible for retreaving all data from any  table in the database 
        
         keys :
            table(str): database table name
            columns(list): list of the columns to fetch. json columns are accessed using the `/` separator eg `other/bio/contacts[0]`
            condition(str): a string indicating the SQL condition for the fetch eg `userId=? and dateCreated<?`. all values a represented with the `?` placeholder
            conditionData(list): a list containing the values for each `?` placeholder in the condition
            limit(int): number indicating the maximum number of results to fetch
            returnDicts(bool): if `True`, we shall return a list of dictionaries as opposed to a list of tuples
            returnNamespaces(bool): if `True`, we shall return a list of named-tuples as opposed to a list of tuples
                ** if both `returnDicts` and `returnNamespaces` are set, `returnDicts` is effected
            parseJson(bool):if `True`, we shall parse json objects to python lists and dictionaries where possible
            returnGenerator(bool): if True, a generator will be returned instead of the list of tuple|dict|SimpleNamespace. this is especially recommended for large data
        
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    with kutils.db.Api(dbPath,tables, readonly=True) as db:
        fetchResponse = db.fetch(tableDetails['tableName'],tableDetails['columns'],tableDetails['condition'],
                                 tableDetails['conditionalData'],limit=tableDetails['limit'],returnDicts=tableDetails['returnDicts'],
                                 returnNamespaces=tableDetails['returnNamespaces'],parseJson=tableDetails['parseJson'],
                                 returnGenerator=False)
        if not len(fetchResponse):
            return {'status':False,
                    'log':f'no registered data realted to instructions provided in table {tableDetails["tableName"]}'}
        return {'status':True,'data':fetchResponse}
    return {'status':False,'log':fetchResponse}
    
# --- below is the disbursemnt databse insertion logic
def insertDataIntoDisbursement(disbursementDetails: dict) -> dict:
    '''
    this module is responsible for inserting data into the table disbursement
    
    @ param `disbursementDetails` : dictionary with expected keys:
        - `budgetId` (str): Reference to budget record
        - `disbursementDate` (str): Date of disbursement (YYYY-MM-DD)
        - `amountReleased` (int): Disbursed amount in USD
        - `paymentMethod` (str): e.g., "Bank Transfer", "Cheque"
        - `disbursementOfficer` (str): Officer responsible
        - `department` (str): Department receiving funds
        - `status` (str): e.g., "Pending", "Completed", "Rejected"
        - `others` (json): Additional metadata
    
    @ return : dictionary with:
        - `status` (bool): True if successful, False if failed
        - `log` (str): Error message if status=False
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    entryId = 'dID' + kutils.codes.new(8)  # Generate unique ID
    timestamp = kutils.dates.currentTimestamp()
    quaterId = utils.quarterIdForExpense({'dateOfExpense':disbursementDetails['disbursementDate']})['data']['quaterId']
    # quaterId = quarter_id['quarterId']
    with kutils.db.Api(dbPath, tables, readonly=False) as db:
        insertionResponse = db.insert(
            'disbursment',
            [
                entryId,
                disbursementDetails['budgetId'],
                quaterId,
                timestamp,
                disbursementDetails['disbursementDate'],
                disbursementDetails['amountReleased'],
                disbursementDetails['paymentMethod'],
                disbursementDetails['disbursementOfficer'],
                disbursementDetails['department'],
                disbursementDetails['status'],
                disbursementDetails.get('others', {})  # Optional field
            ]
        )
        return insertionResponse
    
# ---below is the expense database logic --
def insertDataIntoExpenditure(expenditureDetails: dict) -> dict:
    '''
    this module is responsible for inserting data into the table expenditure
    
    @ param `expenditureDetails` : dictionary with expected keys:
        - `budgetId` (str): Reference to budget record
        - `quaterId` (str): Financial quarter identifier (e.g., "Q1-2023")
        - `dateOfExpense` (str): Date expense occurred (YYYY-MM-DD)
        - `amountSpent` (int): Expenditure amount in USD
        - `detailsOfExpense` (json): Breakdown of expense items
        - `beneficially` (str): Recipient of funds
        - `description` (str): Purpose of expenditure
        - `evidence` (str): Reference to supporting document
        - `others` (json): Additional metadata (optional)
    
    @ return : dictionary with:
        - `status` (bool): True if successful, False if failed
        - `log` (str): Error message if status=False
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    entryId = 'eID' + kutils.codes.new(8)  # Generate unique expenditure ID
    timestamp = kutils.dates.currentTimestamp()
    quaterId = utils.quarterIdForExpense({'dateOfExpense':expenditureDetails['dateOfExpense']})['data']['quaterId']
    with kutils.db.Api(dbPath, tables, readonly=False) as db:
        insertionResponse = db.insert(
            'expenditure',
            [
                entryId,
                expenditureDetails['budgetId'],
                quaterId,
                timestamp,
                expenditureDetails['dateOfExpense'],
                expenditureDetails['amountSpent'],
                expenditureDetails['detailsOfExpense'],
                expenditureDetails['beneficially'],
                expenditureDetails['description'],
                expenditureDetails['evidence'],
                expenditureDetails.get('others', {})  # Optional field
            ]
        )
        return insertionResponse
    
# the modules below are responsible for handling the budget quarters logic 
def insertDataIntoBudgetQuaters(budgetQuaterDetails: dict) -> dict:
    '''
    this module is responsible for inserting data into the table budgetQuaters
    
    @ param `budgetQuaterDetails` : dictionary with expected keys:
        - `budgetId` (str): Reference to parent budget record
        - `quaterId` (str): Quarter identifier (e.g., "Q1-2023")
        - `startDate` (str): Quarter start date (YYYY-MM-DD)
        - `endDate` (str): Quarter end date (YYYY-MM-DD)
        - `others` (json): Additional metadata (optional)
    
    @ return : dictionary with:
        - `status` (bool): True if successful, False if failed
        - `log` (str): Error message if status=False
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    entryId = 'qID' + kutils.codes.new(8)  # Generate unique quarter entry ID
    timestamp = kutils.dates.currentTimestamp()
    quaterId = 'qId' + kutils.codes.new(6)
    
    with kutils.db.Api(dbPath, tables, readonly=False) as db:
        insertionResponse = db.insert(
            'budgetQuaters',
            [
                entryId,
                budgetQuaterDetails['budgetId'],
                timestamp,
                quaterId,
                budgetQuaterDetails['startDate'],
                budgetQuaterDetails['endDate'],
                budgetQuaterDetails.get('others', {})  # Optional field
            ]
        )
        return insertionResponse
    
def getQuartersByBudgetId(budgetId: str) -> dict:
    """
    Retrieves all quarters associated with a specific budgetId
    
    Args:
        budgetId (str): The budget ID to filter quarters
        
           
    Returns:
        dict: {
            'status': bool, 
            'data': list[dict] if status=True, 
            'log': str if status=False
        }
        
    """
    return getAnyTableData({
        'tableName': 'budgetQuaters',
        'columns': ['*'],
        'condition': 'budgetId = ?',
        'conditionalData': [budgetId],
        'limit':4,
        'returnDicts': True,
        'returnNamespaces': False,
        'parseJson': True,
        'returnGenerator': False 
        
    })    
    
def getDisbursementsByBudgetQuarter(budgetId: str, quaterId: str) -> dict:
    """
    Retrieves all disbursements for a specific budget and quarter
    
    Args:
        budgetId (str): The budget ID to filter disbursements
        quaterId (str): The quarter ID to filter disbursements
        
    Returns:
        dict: {
            'status': bool, 
            'data': list[dict] if status=True, 
            'log': str if status=False
        }
        
    """
    return getAnyTableData({
        'tableName': 'disbursment',  
        'columns': ['*'],
        'condition': 'budgetId = ? AND quaterId = ?',
        'conditionalData': [budgetId, quaterId],
        'limit':100,
        'returnDicts': True,
        'returnNamespaces': False,
        'parseJson': True,
        'returnGenerator': False 
    })
    
def getExpendituresByBudgetQuarter(budgetId: str, quaterId: str) -> dict:
    """
    Retrieves all expenditures for a specific budget and quarter
    
    Args:
        budgetId (str): The budget ID to filter expenditures
        quaterId (str): The quarter ID to filter expenditures
        
    Returns:
        dict: {
            'status': bool, 
            'data': list[dict] if status=True, 
            'log': str if status=False
        }
    """
    return getAnyTableData({
        'tableName': 'expenditure',
        'columns': ['*'],
        'condition': 'budgetId = ? AND quaterId = ?',
        'conditionalData': [budgetId, quaterId],
        'limit':100,
        'returnDicts': True,
        'returnNamespaces': False,
        'parseJson': True,
        'returnGenerator': False 
    })
# the modules below are responsible for performance table logic 
def insertDataIntoPerformance(performanceDetails: dict) -> dict:
    '''
    this module is responsible for inserting data into the table performance
    
    @ param `performanceDetails` : dictionary with expected keys:
        - `budgetId` (str): Reference to budget record
        - `quaterId` (str): Financial quarter identifier (e.g., "Q1-2023")
        - `plannedOutputs` (str): Expected deliverables
        - `actualAchievement` (str): Completed deliverables
        - `variance` (str): Performance difference
        - `standardDeviation` (str): Statistical measure of variation
        - `description` (str): Performance analysis notes
        - `others` (json): Additional metadata (optional)
    
    @ return : dictionary with:
        - `status` (bool): True if successful, False if failed
        - `log` (str): Error message if status=False
    '''
    dbPath = kutils.config.getValue('bbmsDb/dbPath')
    tables = kutils.config.getValue('bbmsDb/tables')
    entryId = 'pID' + kutils.codes.new(8)  # Generate unique performance ID
    timestamp = kutils.dates.currentTimestamp()
    
    with kutils.db.Api(dbPath, tables, readonly=False) as db:
        insertionResponse = db.insert(
            'performance',
            [
                entryId,
                performanceDetails['budgetId'],
                performanceDetails['quaterId'],
                timestamp,
                performanceDetails['plannedOutputs'],
                performanceDetails['actualAchievement'],
                performanceDetails['variance'],
                performanceDetails['standardDeviation'],
                performanceDetails['description'],
                performanceDetails.get('others', {})  # Optional field
            ]
        )
        return insertionResponse
def init():
    defaults = {
        'rootPath':'/workspaces/budgetMornitoringSystem/budgetMonitoring',
        'dbName':'bbms',
        'tables':{
             'fundDetails':'''
                            fundId          integer PRIMARY KEY,
                            fund            varchar(32)  NOT NULL
            ''',
             'typesOfFundingSource':'''
                                fundId       integer PRIMARY KEY,
                                type         varchar(255)  NOT NULL
            ''',
            'domesticFundSource':'''
                                    fundId              integer PRIMARY KEY,
                                    domesticGovernment   varchar(255) NOT NULL
            ''',
            'commercialBankFundSources':'''
                                fundId                      integer PRIMARY KEY,
                                commercialBankSources       varchar(255)  NOT NULL
            ''',
            'multiLateralDevelopmentPartners':'''
                                                fundId      varchar(255) PRIMARY KEY,
                                                partner    varchar(255)  NOT NULL
            ''',
              'biLateralDevelopmentPartners':'''
                                                fundId      varchar(255) PRIMARY KEY,
                                                partner    varchar(255)  NOT NULL
            ''',
                'programs':'''
                                                programId      varchar(255) PRIMARY KEY,
                                                program       varchar(255)  NOT NULL
            ''',
                'voteCostCenterMinistries':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                ministry    varchar(255)  NOT NULL
            ''',
             'voteCostCenterAgencies':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                agency    varchar(255)  NOT NULL
            ''',
             'voteCostCenterPusatis':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                pusati      varchar(255)  NOT NULL
            ''',
             'voteCostCenterRefferalHospitals':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                hospital    varchar(255)  NOT NULL
            ''',
             'voteCostCenterEmbassies':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                embassy     varchar(255)  NOT NULL
            ''',
               'voteCostCenterCities':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                city     varchar(255)  NOT NULL
            ''',
               'voteCostCenterMunicipal':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                mucipality     varchar(255)  NOT NULL
            ''',
               
               'voteCostCenterDistricts':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                district     varchar(255)  NOT NULL
            ''',
               'voteCostCenterLocation':'''
                                                voteId      varchar(255) PRIMARY KEY,
                                                location     varchar(255)  NOT NULL
            ''',
                'revenueSummary':'''
                                                classId      INTEGER PRIMARY KEY,
                                                revenueSummary     varchar(255)  NOT NULL
            ''',
                'expenditureSummary':'''
                                                classId      INTEGER PRIMARY KEY,
                                                expensesSummary     varchar(255) NOT NULL
            ''',
                'assetsSummary':'''
                                                classId      INTEGER PRIMARY KEY,
                                                assetsSummary     varchar(255)  NOT NULL
            ''',
                'liabilitiesSummary':'''
                                                classId      INTEGER PRIMARY KEY,
                                                liabilitiesSummary     varchar(255)  NOT NULL
            ''',
            'reservesSummary':'''
                                                classId      INTEGER PRIMARY KEY,
                                                reservesSummary     varchar(255)  NOT NULL
            ''',
            'clearingAccounts':'''
                                                classId      INTEGER PRIMARY KEY,
                                                clearingAccounts     varchar(255)  NOT NULL
            ''',
            
            'users':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            userId              varchar(32) UNIQUE not null,
                            userName            varchar(32) not null,
                            password            varchar(32) not null,
                            phoneNumber         integer(32) PRIMARY KEY,
                            email               varchar(32) UNIQUE not null,
                            roleId              varchar(32)  not null,
                            others              json
            ''',
             'roles':'''
                            entryId             varchar(32) not null,
                            timestamp           varchar(32) not null,
                            roleId              varchar(32) PRIMARY KEY ,
                            role                varchar(32) UNIQUE not null,
                            others              json
                            ''',
               'revokeduser':'''
                                entryId     varchar(32) not null,
                                timestamp   varchar(32) not null,
                                userId      varchar(32) PRIMARY KEY ,
                                userName    varchar(32) not null,
                                password    varchar(32) not null,
                                phoneNumber integer(32) not null,
                                email       varchar(32) UNIQUE not null,
                                roleId      varchar(32) not null,
                                others       json
                
                ''',
                'budget':'''
                            
                                budgetId            varchar(32) PRIMARY KEY,
                                timestamp           varchar(32) not null,
                                dateOfApproval      varchar(32) not null,
                                planned            integer(32) not null,
                                working            integer(32) not null,
                                department          varchar(32) not null,
                                programme           varchar(32) not null,
                                vote                varchar(32) not null,
                                detailsOfBudget    json not null,
                                description         varchar(255) not null,
                                others              json
                
                ''',
                'requisition':'''
                                entryId             varchar(32) not null,
                                budgetId            varchar(32) not null,
                                timestamp           varchar(32) not null,
                                requisitionDate      varchar(32) not null,
                                amountRequested      integer(32) not null,
                                purporse            varchar(32) not null,
                                requestingOfficer   varchar(32) not null,
                                ApprovingOfficer    varchar(32),
                                status              varchar(32) not null,
                                others              json
                
                ''',
                'disbursment':'''
                                entryId             varchar(32) not null,
                                budgetId            varchar(32) not null,
                                quaterId            varchar(32) not null,
                                timestamp           varchar(32) not null,
                                disbursmentDate      varchar(32) not null,
                                amountReleased      integer(32) not null,
                                payementMethod      varchar(32) not null,
                                dispursementOfficer   varchar(32) not null,
                                department            varchar(32) not null,
                                status                 varchar(32) not null,
                                others                 json
                
                ''',
                'expenditure':'''
                                entryId             varchar(32) not null,
                                budgetId            varchar(32) not null,
                                quaterId            varchar(32) not null,
                                timestamp           varchar(32) not null,
                                dateOfExpense       varchar(32) not null,
                                amountSpent          integer(32) not null,
                                detailsOfexpense       json not null,
                                beneficially         varchar(32) not null,
                                description           varchar(32) not null,
                                evidence              varchar(32)not null,
                                others                 json
                
                ''',
                'performance':'''
                                entryId                 varchar(32) not null,
                                budgetId                varchar(32) not null,
                                quaterId                varchar(32) not null,
                                timestamp               varchar(32) not null,
                                plannedOutputs          varchar(32) not null,
                                actualAchievent         varchar(32) not null,
                                variance                varchar(32) not null,
                                stardandDeviation       varchar(32) not null,
                                description             varchar(32) not null,
                                others                  json
                                ''',
                'budgetQuaters':'''
                                entryId                 varchar(32) not null,
                                budgetId                varchar(32) not null,
                                timestamp               varchar(32) not null,
                                quaterId                varchar(32) UNIQUE not null,
                                startDate               varchar(32) not null,
                                endDate                 varchar(32) not null,
                                others                  json
                                '''
        }
    }
    defaults['dbPath'] = defaults['rootPath']+'/db/'+defaults['dbName']
    config_topic = 'bbmsDb'
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic+'/'+key):
            kutils.config.setValue(config_topic+'/'+key,defaults[key])
init()
    
if __name__ == '__main__':
    chartsOfAccountsData = {
    "fundDetails": chartsOfAccounts.fundDetails,
    "domesticFundingSource": chartsOfAccounts.domesticFundingSource,
    "commercialBankSources": chartsOfAccounts.commercialBankSources,
    "expenditureSummary": chartsOfAccounts.expenditureSummary,
    "liabilitiesSummary": chartsOfAccounts.liabilitiesSummary,
    "multiLateralDevelopmentPartners": chartsOfAccounts.multiLateralDevelopmentPartners,
    "programs": chartsOfAccounts.programs,
    "reservesSummary": chartsOfAccounts.reservesSummary,
    "revenueSummary": chartsOfAccounts.revenueSummary,
    "voteCostCenterAgencies": chartsOfAccounts.voteCostCenterAgencies,
    "voteCostCenterCities": chartsOfAccounts.voteCostCenterCities,
    "voteCostCenterDistricts": chartsOfAccounts.voteCostCenterDistricts,
    "voteCostCenterEmbassies": chartsOfAccounts.voteCostCenterEmbassies,
    "voteCostCenterLocation": chartsOfAccounts.voteCostCenterLocation,
    "voteCostCenterMinistries": chartsOfAccounts.voteCostCenterMinistries,
    "voteCostCenterMunicipal": chartsOfAccounts.voteCostCenterMunicipal,
    "voteCostCenterRefferalHospitals": chartsOfAccounts.voteCostCenterRefferalHospitals,
    "voteCostCenterrefferalPusatis": chartsOfAccounts.voteCostCenterrefferalPusatis,
    "clearingAccounts": chartsOfAccounts.clearingAccounts,
    "biLateralDevelopmentPartners": chartsOfAccounts.biLateralDevelopmentPartners
}
    import pprint
    print(createTables())
    # insertData = makeDataInserter()
    # for table , account in chartsOfAccountsData.items():
    #     insertData(table,account)
       
            
 