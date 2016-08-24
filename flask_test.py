from flask import Flask, request
app = Flask(__name__)

# Testing command: curl --data "var=test123" http://localhost:5000
@app.route("/", methods=["GET","POST"])
def hello():
  if request.method == 'POST':
    print "Got: " + request.form['var']
    return '1'
  else:
    return '0'

if __name__ == "__main__":
  app.run()
