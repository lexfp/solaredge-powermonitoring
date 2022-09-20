import requests
import boto3


def lambda_handler(event, context):

    response = requests.get("https://monitoringapi.solaredge.com/site/SITE_ID/overview.json?api_key=REPLACE_WITH_SOLAREDGE_API_KEY")

    message = ""
    try:
        power = response.json()["overview"]["lastDayData"]["energy"]
        message = message + "Power generation: "+str(power)+". "
        if (int(power) < 1):
            message += "No power generation today."
            send_mail(message)
    except Exception:
        message = "Error retrieving power output for today."
        send_mail(message)

    body = {
        "message": message,
        "rsp": response.text
    } 

    return {"statusCode": 200, "body": message}

def send_mail(body):
    
    ses = boto3.client('ses')
    body += "\n\nGenerated from AWS Lambda."

    ses.send_email(
	    Source = 'FROM@EMAIL.COM',
	    Destination = {
		    'ToAddresses': [
			    'TO@EMAIL.COM'
		    ]
	    },
	    Message = {
		    'Subject': {
			    'Data': 'Solaredge Power Monitoring',
			    'Charset': 'UTF-8'
		    },
		    'Body': {
			    'Text':{
				    'Data': body,
				    'Charset': 'UTF-8'
			    }
		    }
	    }
    )