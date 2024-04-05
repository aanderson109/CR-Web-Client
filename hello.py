from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

# configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"UserInput('{self.content}')"

class Entry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(100), nullable=False)
    system = db.Column(db.String(100), nullable=False)
    vendor = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Entry('{self.id}', '{self.submission_date}', '{self.type}', '{self.system}', '{self.vendor}', '{self.name}', '{self.description}', '{self.status}', '{self.comments}')"

# function to query CVEs
def query_cves(vendor, name):

    # base URL link for CVE API from nvd.nist.gov
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "vendor": vendor,
        "product": name
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()  # assuming the API returns JSON data
    else:
        return None

# route definitions
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # assuming you'r ehandling entry form submissions
        entry = Entry(
            type=request.form['type'],
            system=request.form['system'],
            vendor=request.form['vendor'],
            name=request.form['name'],
            description=request.form['description'],
            status=request.form['status'],
            comments=request.form.get('comments', '')
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('home'))
    # if you want to display both UserInputs and Entries, you must query both and pass them to your template
    inputs = UserInput.query.all()
    entries = Entry.query.all()
    return render_template('index.html', inputs=inputs, entries=entries)

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if request.method == 'POST':
        entry.type = request.form['type']
        entry.system = request.form['system']
        entry.vendor = request.form['vendor']
        entry.name = request.form['name']
        entry.description = request.form['description']
        entry.status = request.form['status']
        entry.comments = request.form.get('comments', '')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/query_cves/<int:entry_id>')
def query_entry_cves(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    cves = query_cves(entry.vendor, entry.name)
    return render_template("cve_results.html", cves=cves, entry=entry)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
