from flask import Flask,request,jsonify,session, redirect, url_for,render_template,make_response,send_file
# from flask_sqlalchemy import SQL
from functools import wraps
from flask_cors import CORS
import kisa_utils as kutils
#import jwt
from datetime import datetime, timedelta
# from auth_utils import generate_token, decode_token
from flask_mail import Mail, Message
from datetime import datetime
from openpyxl import Workbook

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = kutils.config.getValue('bbmsDb/SECRETE_KEY')
# Configure Flask-Mail with your SMTP server details
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 #465 
app.config['MAIL_USERNAME'] = kutils.config.getValue('bbmsDb/SMTPemail')
app.config['MAIL_PASSWORD'] = kutils.config.getValue('bbmsDb/mailPassword')  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 

mail = Mail(app)

@app.route("/sendMail", methods=['POST'])
def sendMail():
    '''
    This endpoint is responsible for sending emails
    '''
    payload = request.get_json()
    if not payload:
        return jsonify({'status': False, 'log': 'Payload is missing or invalid'})
    
    print(f"Payload received: {payload}")
    
    payloadStructure = {
        'subject': kutils.config.getValue('bmsDb/subject'),
        'recipients': kutils.config.getValue('bmsDb/recipients'),
        'message': kutils.config.getValue('bmsDb/message')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    # print(f"Payload validation status: {payloadValidationResponse['status']}")
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({'status': False, 'log': f"The value for {key} is missing, please provide it"})
        
        # print(f"Recipients: {payload.get('recipients')}")
        
        
        for recipient in payload['recipients']:
            # print('>>>> Running recipient loop')
            if not isinstance(recipient, str):
                return jsonify({'status': False, 'log': f"The recipient {recipient} expects strings in the list"})
        
        msg = Message(
            payload['subject'],
            sender='your business Point Of Sale System',
            recipients=payload['recipients']
        )
        msg.body = payload['message']
        
        with app.app_context():
            mail.send(msg)
        
        return jsonify({'status': True, 'log': ''})
    
    return jsonify(payloadValidationResponse)

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
            sender= kutils.config.getValue('bbmsDb/MAIL_DEFAULT_SENDER'),
            recipients=mailDetails['recipients']
        )
        msg.body = mailDetails['message']
        
        with app.app_context():  # Only need one context
            mail.send(msg)
            
        return {'status': True, 'log': 'Email sent successfully'}
        
    except Exception as e:
        return {'status': False, 'log': f'Failed to send email: {str(e)}'}
@app.route('/')
def home():
    # create the database tables if they don't exist 
    from db import createTables
    createTables()
    
    # Renders the index.html file located in the templates folder
    
    return render_template('index.html')

# ------the module below is responsible fo handling user and roles  related endpoints 
@app.route('/getQuarterMetrics',methods=['POST'])
def handleQuarterMetrics():
    from utils import getQuarterlyPerfromanceMetric
    
    payload = request.get_json()
    payloadStructure = {
        'budgetId' : kutils.config.getValue('bbmsDb/budgetId')
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
         for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
                
         metrics = getQuarterlyPerfromanceMetric(payload['budgetId'])
         return metrics 
     
@app.route('/getSingleQuarterMetrics',methods=['POST'])
def handleSingleQuarterMetrics():
    from utils import getQuarterlyPerfromanceMetric
    
    payload = request.get_json()
    payloadStructure = {
        'budgetId' : kutils.config.getValue('bbmsDb/budgetId'),
        'quaterMonthDate':kutils.config.getValue('bbmsDb/quaterMonthDate')
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    
    if validationResponse['status']:
         for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
                
         metrics = getQuarterlyPerfromanceMetric(payload['budgetId'])
         return metrics 

     
@app.route('/adduser',methods=['POST'])
# @role_required(['MANAGER'])
def handleAdduser():
    '''
    this function is responsible for handling 
    the adduser endpoint 
    '''
    from db import createUser
    payload = request.get_json()
    payload['entryId'] = kutils.codes.new()
    payload['userId'] = kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payloadStructure = {
        'entryId':kutils.config.getValue('bbmsDb/entryId'),
        'timestamp':kutils.config.getValue('bbmsDb/timestamp'),
        'userId':kutils.config.getValue('bbmsDb/userId'),
        'userName':kutils.config.getValue('bbmsDb/userName'),
        'password':kutils.config.getValue('bbmsDb/password'),
        'email':kutils.config.getValue('bbmsDb/email'),
        'phoneNumber':kutils.config.getValue('bbmsDb/phoneNumber'),
        'others':kutils.config.getValue('bbmsDb/others'),
        'roleId':kutils.config.getValue('bbmsDb/roleId')
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    print('>>',validationResponse)
    print('>>>>',payload)
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({
                    'status': False,
                    'log': f'The value for {key} is missing. Please provide it.'
                })
        
        createUserResponse  = createUser(payload)
        
        if createUserResponse['status']:
            mailResponse = sendDynamicMail({'recipients':[payload['email']],
                                            'message':f'Your account hasbeen created in the bbms and your password is 1234 and username is {payload["userName"]}',
                                            'subject':"account creation in the BBMS "})
            if mailResponse['status']:
                return createUserResponse
            
            
        return jsonify(createUserResponse)
    
    return jsonify(validationResponse)




def init():
    
        defaults = {
            'recipients':list,
            'message':str,
            'subject':str,
            'entryId':str,
            'productId':str,
            'timestamp':str,
            'userId':str,
            'userId':str,
            'userName':str,
            'phoneNumber':str,
            'roles':str,
            'email':str,
            'roleId':str,
            'password':str,
            'role':str,
            'others':dict,
            'budgetId':str,
            'quaterMonthDate':str,
            'SECRETE_KEY':kutils.codes.new(),
            'SESSION_TYPE':'filesystem',
            'SESSION_PERMANENT':False,
            'SESSION_user_SIGNER':True,
            'SMTPemail':'adamzhakeam@gmail.com',
            'mailPassword': 'xgff xigx wcvp swzb ', #'xzhf bphb kwuz ybzj',
            'MAIL_DEFAULT_SENDER': ('BBMS System', 'adamzhakeam@gmail.com')
            
        }
        config_topic = 'bbmsDb'
        
        for key in defaults:
            if 1 or not kutils.config.getValue(config_topic+'/'+key):
                kutils.config.setValue(config_topic+'/'+key,defaults[key])
                
init()

if __name__ == "__main__":
    # print(sendDynamicMail({'recipients':['kisiturashid01@gmail.com'],'message':'massage','subject':'work'}))
     app.run(debug=True,host = '0.0.0.0',port = 5000)
    #  app.run(debug=True,host = '0.0.0.0',port = 8080) but the am getting this error predator@predator ~/D/p/budgetMonitoring> python3 app.py

# {'status': False, 'log': "Failed to send email: (530, b'5.7.0 Authentication Required. For more information, go to\\n5.7.0  https://support.google.com/accounts/troubleshooter/2402620. 5b1f17b1804b1-4587054f22esm190107285e9.9 - gsmtp', '=?utf-8?q?BBMS_System?= <adamzhakeam@gmail.com>')"}
