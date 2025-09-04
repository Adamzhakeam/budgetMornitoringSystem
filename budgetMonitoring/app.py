# Import from kisa_utils servers instead of directly from Flask
from kisa_utils.servers.flask import endpoint, SecurityPolicy, Response, Ok, Error, getAppInstance, startServer
from kisa_utils.structures.validator import Value
from flask import render_template, request
from flask_mail import Mail, Message
from flask_cors import CORS
import kisa_utils as kutils
from datetime import datetime
from openpyxl import Workbook

# Initialize the app using Kisa's utilities
app = getAppInstance()
CORS(app)

# Your existing configuration
app.config['SECRET_KEY'] = kutils.config.getValue('bbmsDb/SECRETE_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = kutils.config.getValue('bbmsDb/SMTPemail')
app.config['MAIL_PASSWORD'] = kutils.config.getValue('bbmsDb/mailPassword')  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Authentication validator function
def validate_credentials(username: str, password: str) -> Response:
    """
    Validate basic auth credentials for API documentation access
    """
    # Implement your actual authentication logic here
    if username == "admin" and password == "password123":
        return Ok()
    return Error("Invalid credentials")

# SendMail endpoint using Kisa utilities
@endpoint(
    name='sendMail',
    methods=['POST'],
    security=SecurityPolicy.basic_auth(validate_credentials)
)
def sendMail(*, subject: str, recipients: list, message: str) -> Response:
    '''
    This endpoint is responsible for sending emails
    '''
    for recipient in recipients:
        if not isinstance(recipient, str):
            return Error(f"The recipient {recipient} expects strings in the list")
    
    msg = Message(
        subject,
        sender='your business Point Of Sale System',
        recipients=recipients
    )
    msg.body = message
    
    try:
        mail.send(msg)
        return Ok({"status": True, "log": "Email sent successfully"})
    except Exception as e:
        return Error(f"Failed to send email: {str(e)}")

# Helper function for sending emails
def sendDynamicMail(mailDetails: dict) -> dict:
    '''
    Send emails with proper error handling
    Expected keys: 'recipients', 'message', 'subject'
    '''
    if not mailDetails.get('recipients'):
        return {'status': False, 'log': 'No recipients provided'}
    
    try:
        msg = Message(
            subject=mailDetails['subject'],
            sender=kutils.config.getValue('bbmsDb/MAIL_DEFAULT_SENDER'),
            recipients=mailDetails['recipients']
        )
        msg.body = mailDetails['message']
        
        mail.send(msg)
        return {'status': True, 'log': 'Email sent successfully'}
    except Exception as e:
        return {'status': False, 'log': f'Failed to send email: {str(e)}'}

# Home endpoint
@app.route('/')
def home():
    from db import createTables
    createTables()
    return render_template('index.html')

# ... (keep your imports and setup code the same)

# Quarter metrics endpoint
@endpoint(
    name='getQuarterMetrics',
    methods=['POST'],
    group='metrics'
)
def handleQuarterMetrics(*, budgetId: str) -> Response:
    '''
    Retrieve quarterly performance metrics for a specific budget
    Args:
        budgetId (str): The ID of the budget to get metrics for
    Returns:
        Quarterly performance metrics for the specified budget
    '''
    from utils import getQuarterlyPerfromanceMetric
    metrics = getQuarterlyPerfromanceMetric(budgetId)
    return Ok(metrics) if metrics.get('status') else Error(metrics.get('log', 'Unknown error'))

# Single quarter metrics endpoint
@endpoint(
    name='getSingleQuarterMetrics',
    methods=['POST'],
    group='metrics'
)
def handleSingleQuarterMetrics(*, budgetId: str, quaterMonthDate: str) -> Response:
    '''
    Retrieve performance metrics for a specific quarter of a budget
    Args:
        budgetId (str): The ID of the budget to get metrics for
        quaterMonthDate (str): The month date identifying the specific quarter
    Returns:
        Performance metrics for the specified budget quarter
    '''
    from utils import getSingleQuarterlyPerfromanceMetric
    metrics = getSingleQuarterlyPerfromanceMetric(budgetId, quaterMonthDate)
    return Ok(metrics) if metrics.get('status') else Error(metrics.get('log', 'Unknown error'))

# Chart account search endpoint
@endpoint(
    name='getAnyChartAccount',
    methods=['POST'],
    group='accounts'
)
def handleSearchAnyChartAccount(*, accountName: str) -> Response:
    '''
    Search for chart accounts by name
    Args:
        accountName (str): The name of the account to search for
    Returns:
        Matching chart accounts based on the search criteria
    '''
    from db import getAnyChartAccount
    matches = getAnyChartAccount(accountName)
    return Ok(matches) if matches.get('status') else Error(matches.get('log', 'Unknown error'))

# Add budget endpoint
@endpoint(
    name='addBudget',
    methods=['POST'],
    group='budgets'
)
def handleAddBudget(
    *, 
    department: str, 
    vote: str, 
    programme: str, 
    working: int, 
    planned: int,
    dateOfApproval: str, 
    detailsOfBudget: dict, 
    description: str, 
    others: dict
) -> Response:
    '''
    Add a new budget to the system
    Args:
        department (str): The department associated with the budget
        vote (str): The vote code for the budget
        programme (str): The programme associated with the budget
        working (int): The working budget amount
        planned (int): The planned budget amount
        dateOfApproval (str): The date when the budget was approved
        detailsOfBudget (dict): Additional details about the budget
        description (str): Description of the budget
        others (dict): Any other relevant information
    Returns:
        Confirmation of budget creation with status and details
    '''
    from db import insertDataIntoBudget
    
    budget_data = {
        'department': department,
        'vote': vote,
        'programme': programme,
        'working': working,
        'planned': planned,
        'dateOfApproval': dateOfApproval,
        'detailsOfBudget': detailsOfBudget,
        'description': description,
        'others': others
    }
    
    createBudgetResponse = insertDataIntoBudget(budget_data)
    return Ok(createBudgetResponse) if createBudgetResponse.get('status') else Error(createBudgetResponse.get('log', 'Unknown error'))

# Add quarter endpoint
@endpoint(
    name='addQuarter',
    methods=['POST'],
    group='quarters'
)
def handleAddQuarter(*, budgetId: str, startDate: str, endDate: str, others: dict) -> Response:
    '''
    Add a new quarter to a budget
    Args:
        budgetId (str): The ID of the budget to add a quarter to
        startDate (str): The start date of the quarter
        endDate (str): The end date of the quarter
        others (dict): Any other relevant information about the quarter
    Returns:
        Confirmation of quarter creation with status and details
    '''
    from db import insertDataIntoBudgetQuaters
    
    quarter_data = {
        'budgetId': budgetId,
        'startDate': startDate,
        'endDate': endDate,
        'others': others
    }
    
    createQuarterResponse = insertDataIntoBudgetQuaters(quarter_data)
    return Ok(createQuarterResponse) if createQuarterResponse.get('status') else Error(createQuarterResponse.get('log', 'Unknown error'))

# Get budgets endpoint
@endpoint(
    name='getBudget',
    methods=['POST'],
    group='budgets'
)
def handleGetBudgets() -> Response:
    '''
    Retrieve all budgets from the system
    Returns:
        List of all budgets with their details
    '''
    from db import getAnyTableData
    
    fetchResponse = getAnyTableData({
        'tableName': 'budget',
        'columns': ['*'],
        'condition': '',
        'conditionalData': [],
        'limit': 100,
        'returnDicts': True,
        'returnNamespaces': False,
        'parseJson': True,
        'returnGenerator': False
    })
    
    return Ok(fetchResponse) if fetchResponse.get('status') else Error(fetchResponse.get('log', 'Unknown error'))


# Configuration initialization
def init():
    defaults = {
        'recipients': list,
        'message': str,
        'subject': str,
        'entryId': str,
        'productId': str,
        'timestamp': str,
        'userId': str,
        'userName': str,
        'phoneNumber': str,
        'roles': str,
        'email': str,
        'roleId': str,
        'password': str,
        'role': str,
        'others': dict,
        'budgetId': str,
        'quaterMonthDate': str,
        'accountName': str,
        'department': str,
        'vote': str,
        'programme': str,
        'working': int,
        'planned': int,
        'detailsOfBudget': dict,
        'description': str,
        'dateOfApproval': str,
        'startDate': str,
        'endDate': str,
        'SECRETE_KEY': kutils.codes.new(),
        'SESSION_TYPE': 'filesystem',
        'SESSION_PERMANENT': False,
        'SESSION_user_SIGNER': True,
        'SMTPemail': 'adamzhakeam@gmail.com',
        'mailPassword': 'xgff xigx wcvp swzb',
        'MAIL_DEFAULT_SENDER': ('BBMS System', 'adamzhakeam@gmail.com')
    }
    
    config_topic = 'bbmsDb'
    
    for key in defaults:
        if not kutils.config.getValue(f'{config_topic}/{key}'):
            kutils.config.setValue(f'{config_topic}/{key}', defaults[key])

if __name__ == "__main__":
    init()
    startServer(
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        userName='admin',  # For docs authentication
        password='password123'
    )










# from flask import Flask,request,jsonify,session, redirect, url_for,render_template,make_response,send_file
# # from flask_sqlalchemy import SQL
# from functools import wraps
# from flask_cors import CORS
# import kisa_utils as kutils
# # kutils.servers.flask
# #import jwt
# from datetime import datetime, timedelta
# # from auth_utils import generate_token, decode_token
# from flask_mail import Mail, Message
# from datetime import datetime
# from openpyxl import Workbook

# app = Flask(__name__)
# CORS(app)
# app.config['SECRET_KEY'] = kutils.config.getValue('bbmsDb/SECRETE_KEY')
# # Configure Flask-Mail with your SMTP server details
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587 #465 
# app.config['MAIL_USERNAME'] = kutils.config.getValue('bbmsDb/SMTPemail')
# app.config['MAIL_PASSWORD'] = kutils.config.getValue('bbmsDb/mailPassword')  
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False 

# mail = Mail(app)

# @app.route("/sendMail", methods=['POST'])
# def sendMail():
#     '''
#     This endpoint is responsible for sending emails
#     '''
#     payload = request.get_json()
#     if not payload:
#         return jsonify({'status': False, 'log': 'Payload is missing or invalid'})
    
#     print(f"Payload received: {payload}")
    
#     payloadStructure = {
#         'subject': kutils.config.getValue('bmsDb/subject'),
#         'recipients': kutils.config.getValue('bmsDb/recipients'),
#         'message': kutils.config.getValue('bmsDb/message')
#     }
    
#     payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
#     # print(f"Payload validation status: {payloadValidationResponse['status']}")
    
#     if payloadValidationResponse['status']:
#         for key in payload:
#             if not payload[key]:
#                 return jsonify({'status': False, 'log': f"The value for {key} is missing, please provide it"})
        
#         # print(f"Recipients: {payload.get('recipients')}")
        
        
#         for recipient in payload['recipients']:
#             # print('>>>> Running recipient loop')
#             if not isinstance(recipient, str):
#                 return jsonify({'status': False, 'log': f"The recipient {recipient} expects strings in the list"})
        
#         msg = Message(
#             payload['subject'],
#             sender='your business Point Of Sale System',
#             recipients=payload['recipients']
#         )
#         msg.body = payload['message']
        
#         with app.app_context():
#             mail.send(msg)
        
#         return jsonify({'status': True, 'log': ''})
    
#     return jsonify(payloadValidationResponse)

# def sendDynamicMail(mailDetails: dict) -> dict:
#     '''
#     Send emails with proper error handling
#     Expected keys: 'recipients', 'message', 'subject'
#     '''
#     if not mailDetails.get('recipients'):
#         return {'status': False, 'log': 'No recipients provided'}
    
#     try:
#         msg = Message(
#             subject=mailDetails['subject'],
#             sender= kutils.config.getValue('bbmsDb/MAIL_DEFAULT_SENDER'),
#             recipients=mailDetails['recipients']
#         )
#         msg.body = mailDetails['message']
        
#         with app.app_context():  # Only need one context
#             mail.send(msg)
            
#         return {'status': True, 'log': 'Email sent successfully'}
        
#     except Exception as e:
#         return {'status': False, 'log': f'Failed to send email: {str(e)}'}
# @app.route('/')
# def home():
#     # create the database tables if they don't exist 
#     from db import createTables
#     createTables()
    
#     # Renders the index.html file located in the templates folder
    
#     return render_template('index.html')

# # ------the module below is responsible fo handling user and roles  related endpoints 
# @app.route('/getQuarterMetrics',methods=['POST'])
# def handleQuarterMetrics():
#     from utils import getQuarterlyPerfromanceMetric
    
#     payload = request.get_json()
#     payloadStructure = {
#         'budgetId' : kutils.config.getValue('bbmsDb/budgetId')
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
#     if validationResponse['status']:
#          for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
                
#          metrics = getQuarterlyPerfromanceMetric(payload['budgetId'])
#          return metrics 
     
# @app.route('/getSingleQuarterMetrics',methods=['POST'])
# def handleSingleQuarterMetrics():
#     from utils import getSingleQuarterlyPerfromanceMetric
    
#     payload = request.get_json()
#     payloadStructure = {
#         'budgetId' : kutils.config.getValue('bbmsDb/budgetId'),
#         'quaterMonthDate':kutils.config.getValue('bbmsDb/quaterMonthDate')
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
#     if validationResponse['status']:
#          for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
                
#          metrics = getSingleQuarterlyPerfromanceMetric(payload['budgetId'],payload['quaterMonthDate'])
#          return metrics 
     
# @app.route('/getAnyChartAccount',methods=['POST'])
# def handleSearchAnyChartAccount():
#     from db import getAnyChartAccount
    
#     payload = request.get_json()
#     payloadStructure = {
#         'accountName' : kutils.config.getValue('bbmsDb/accountName'),
        
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
#     if validationResponse['status']:
#          for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
                
#          matches = getAnyChartAccount(payload['accountName'])
#          return matches 


     
# @app.route('/adduser',methods=['POST'])
# # @role_required(['MANAGER'])
# def handleAdduser():
#     '''
#     this function is responsible for handling 
#     the adduser endpoint 
#     '''
#     from db import createUser
#     payload = request.get_json()
#     payload['entryId'] = kutils.codes.new()
#     payload['userId'] = kutils.codes.new()
#     payload['timestamp'] = kutils.dates.currentTimestamp()
#     payloadStructure = {
#         'entryId':kutils.config.getValue('bbmsDb/entryId'),
#         'timestamp':kutils.config.getValue('bbmsDb/timestamp'),
#         'userId':kutils.config.getValue('bbmsDb/userId'),
#         'userName':kutils.config.getValue('bbmsDb/userName'),
#         'password':kutils.config.getValue('bbmsDb/password'),
#         'email':kutils.config.getValue('bbmsDb/email'),
#         'phoneNumber':kutils.config.getValue('bbmsDb/phoneNumber'),
#         'others':kutils.config.getValue('bbmsDb/others'),
#         'roleId':kutils.config.getValue('bbmsDb/roleId')
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
#     print('>>',validationResponse)
#     print('>>>>',payload)
#     if validationResponse['status']:
#         for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
        
#         createUserResponse  = createUser(payload)
        
#         if createUserResponse['status']:
#             mailResponse = sendDynamicMail({'recipients':[payload['email']],
#                                             'message':f'Your account hasbeen created in the bbms and your password is 1234 and username is {payload["userName"]}',
#                                             'subject':"account creation in the BBMS "})
#             if mailResponse['status']:
#                 return createUserResponse
            
            
#         return jsonify(createUserResponse)
    
#     return jsonify(validationResponse)

# @app.route('/addBudget',methods=['POST'])
# # @role_required(['MANAGER'])
# def handleAddBudget():
#     '''
#     this function is responsible for handling 
#     the addbudget endpoint 
#     '''
#     from db import insertDataIntoBudget
#     payload = request.get_json()
#     payloadStructure = {
#         'department':kutils.config.getValue('bbmsDb/department'),
#         'vote':kutils.config.getValue('bbmsDb/vote'),
#         'programme':kutils.config.getValue('bbmsDb/programme'),
#         'working':kutils.config.getValue('bbmsDb/working'),
#         'planned':kutils.config.getValue('bbmsDb/planned'),
#         'dateOfApproval':kutils.config.getValue('bbmsDb/dateOfApproval'),
#         'detailsOfBudget':kutils.config.getValue('bbmsDb/detailsOfBudget'),
#         'description':kutils.config.getValue('bbmsDb/description'),
#         'others':kutils.config.getValue('bbmsDb/others')
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
#     print('>>',validationResponse)
#     print('>>>>',payload)
#     if validationResponse['status']:
#         for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
        
#         createUserResponse  = insertDataIntoBudget(payload)
            
            
#         return jsonify(createUserResponse)
    
#     return jsonify(validationResponse)

# @app.route('/addQuarter',methods=['POST'])
# # @role_required(['MANAGER'])
# def handleAddQuarter():
#     '''
#     this function is responsible for handling 
#     the addingQuarter endpoint 
#     '''
#     from db import insertDataIntoBudgetQuaters
#     payload = request.get_json()
#     payloadStructure = {
#         'budgetId':kutils.config.getValue('bbmsDb/budgetId'),
#         'startDate':kutils.config.getValue('bbmsDb/startDate'),
#         'endDate':kutils.config.getValue('bbmsDb/endDate'),
#         'others':kutils.config.getValue('bbmsDb/others')
#     }
#     validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
#     # print('>>',validationResponse)
#     # print('>>>>',payload)
#     if validationResponse['status']:
#         for key in payload:
#             if not payload[key]:
#                 return jsonify({
#                     'status': False,
#                     'log': f'The value for {key} is missing. Please provide it.'
#                 })
        
#         createQuarterResponse  = insertDataIntoBudgetQuaters(payload)
        
            
#         print('>>>>',createQuarterResponse)   
#         return jsonify(createQuarterResponse)
    
#     return jsonify(validationResponse)


# @app.route('/getBudget',methods=['POST'])
# def handleGetBudgets():
#     from db import getAnyTableData
#     # payload = request.get_json()
#     fetchResponse = getAnyTableData(
#         {
#         'tableName': 'budget',
#         'columns': ['*'],
#         'condition': '',
#         'conditionalData': [],
#         'limit':100,
#         'returnDicts': True,
#         'returnNamespaces': False,
#         'parseJson': True,
#         'returnGenerator': False 
        
#     }
#     )
#     return jsonify(fetchResponse)



# def init():
    
#         defaults = {
#             'recipients':list,
#             'message':str,
#             'subject':str,
#             'entryId':str,
#             'productId':str,
#             'timestamp':str,
#             'userId':str,
#             'userId':str,
#             'userName':str,
#             'phoneNumber':str,
#             'roles':str,
#             'email':str,
#             'roleId':str,
#             'password':str,
#             'role':str,
#             'others':dict,
#             'budgetId':str,
#             'quaterMonthDate':str,
#             'accountName':str,
#             'department':str,
#             'vote':str,
#             'programme':str,
#             'working':int,
#             'planned':int,
#             'detailsOfBudget':dict,
#             'description':str,
#             'dateOfApproval':str,
#             'startDate':str,
#             'endDate':str,
#             'SECRETE_KEY':kutils.codes.new(),
#             'SESSION_TYPE':'filesystem',
#             'SESSION_PERMANENT':False,
#             'SESSION_user_SIGNER':True,
#             'SMTPemail':'adamzhakeam@gmail.com',
#             'mailPassword': 'xgff xigx wcvp swzb ', #'xzhf bphb kwuz ybzj',
#             'MAIL_DEFAULT_SENDER': ('BBMS System', 'adamzhakeam@gmail.com')
            
#         }
#         config_topic = 'bbmsDb'
        
#         for key in defaults:
#             if 1 or not kutils.config.getValue(config_topic+'/'+key):
#                 kutils.config.setValue(config_topic+'/'+key,defaults[key])
                
# init()

# if __name__ == "__main__":
#     # print(sendDynamicMail({'recipients':['kisiturashid01@gmail.com'],'message':'massage','subject':'work'}))
#      app.run(debug=True,host = '0.0.0.0',port = 5000)
#     #  app.run(debug=True,host = '0.0.0.0',port = 8080) but the am getting this error predator@predator ~/D/p/budgetMonitoring> python3 app.py

# # {'status': False, 'log': "Failed to send email: (530, b'5.7.0 Authentication Required. For more information, go to\\n5.7.0  https://support.google.com/accounts/troubleshooter/2402620. 5b1f17b1804b1-4587054f22esm190107285e9.9 - gsmtp', '=?utf-8?q?BBMS_System?= <adamzhakeam@gmail.com>')"}
