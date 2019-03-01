import flask
from flask import Flask, request, jsonify,render_template, Response, send_file, send_from_directory, redirect
import check_email

app = Flask(__name__)

@app.route("/")
def process():
	jira_options = {'server': 'https://topkidjira.topica.vn'}
	print("logging in ...")
	jira = JIRA(options = jira_options, basic_auth = ('thehao5297','thehao5297'))
	print("logged in.")
	issue = jira.issue('WOR-10')
	last_status = None
	while True:
	    status = issue.fields.status
	    if status != last_status:
	        if str(status) == 'HL01':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 5d 12h'}}]})
	        elif str(status) == 'HL02 ver 1.0':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 4d 12h'}}]})
	        elif str(status) == 'HL02 ver 1.0 in review':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 3d 12h'}}]})
	        elif str(status) == 'HL02 ver 2.0':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 3d'}}]})
	        elif str(status) == 'HL02 ver 3.0':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 2d 12h'}}]})
	        elif str(status) == 'HL03 ver 1.0':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1w 1d 12h'}}]})
	        elif str(status) == 'HL03 ver 2.0':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '6d 12h'}}]})
	        elif str(status) == 'HL04 in review':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '4d 12h'}}]}) 
	        elif str(status) == 'HL04':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '3d 12h'}}]})
	        elif str(status) == 'HL05 in review':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '2d 12h'}}]})
	        elif str(status) == 'HL05 Done':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1d 12h'}}]})
	        elif str(status) == 'HL06':
	            issue.update(update={"timetracking": [{"edit": {"remainingEstimate": '1d'}}]})
	        else:
	            print("unknown status, status -> {}".format(status))
	    last_status = status

if __name__ == "__main__":
	app.run()