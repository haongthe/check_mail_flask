import flask
from flask import Flask, request, jsonify,render_template, Response, send_file, send_from_directory, redirect
import check_email

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file.filename == "" or file.filename == None:
			print('no file selected!')
			return redirect(request.url)
		else:
			print("RECEIVED file name -> {} ([WARNING]UNTRUSTED)".format(file.filename))
			file.save(file.filename)
			print("PROCESSING FILE DATA... PLEASE WAIT FOR A WHILE...")
			rps, processed_file = check_email.main(file.filename)
			print("{}{}".format(rps, processed_file))
			return redirect("/download/{}".format(processed_file))
			# return render_template('result.html', filename = processed_file)
	return render_template('upload.html')

@app.route("/download/<filename>")
def download(filename):
	return send_file(filename, as_attachment=True, attachment_filename = "TO_CLIENT_" + filename)
if __name__ == "__main__":
	app.run()
