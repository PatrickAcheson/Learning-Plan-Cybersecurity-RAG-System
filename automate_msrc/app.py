from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import datetime, requests, csv, io

app = Flask(__name__)
app.secret_key = 'changeme'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id): self.id = id
USERS = {'admin': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id): return User(user_id) if user_id in USERS else None

API_VERSION='v3.0'
BASE_URL=f'https://api.msrc.microsoft.com/cvrf/{API_VERSION}/cvrf/'
HEADERS={'Accept':'application/json'}

def current_ym():
    return datetime.datetime.now().strftime("%Y-%b")

def fetch_vulns():
    r = requests.get(BASE_URL + current_ym(), headers=HEADERS)
    r.raise_for_status()
    return r.json().get('Vulnerability') or []

def cve_sections():
    vulns = fetch_vulns()
    allv, crit, exploited, likely = [], [], [], []
    for v in vulns:
        score = max((float(s.get('BaseScore', 0)) for s in v.get('CVSSScoreSets') or []), default=0)
        title = v.get('Title', {}).get('Value', '')
        cve = v.get('CVE', '')
        remediation = next((r.get('URL') for r in v.get('Remediations') or [] if r.get('URL')), '')
        threats = v.get('Threats') or []
        act = any(t.get('Type') == 1 and 'Exploited:Yes' in t.get('Description', {}).get('Value', '') for t in threats)
        likelyx = any(t.get('Type') == 1 and 'exploitation more likely' in t.get('Description', {}).get('Value', '').lower() for t in threats)
        tags = []
        if score >= 9.0: tags.append("Critical")
        elif score >= 7.0: tags.append("Important")
        if act: tags.append("Exploited")
        if likelyx: tags.append("Likely Exploited")
        item = {
            'cve': cve,
            'title': title,
            'remediation': remediation,
            'link': f"https://nvd.nist.gov/vuln/detail/{cve}",
            'score': score,
            'is_critical': score >= 9.0,
            'is_exploited': act,
            'is_likely': likelyx,
            'tags': tags,
            'desc': next((n.get('Value') for n in v.get('Notes') or [] if str(n.get('Type','')).lower()=='description'), ''),
        }
        allv.append(item)
        if item['is_critical']: crit.append(item)
        if item['is_exploited']: exploited.append(item)
        if item['is_likely']: likely.append(item)

    allv = sorted(allv, key=lambda x: x['score'], reverse=True)
    crit = sorted(crit, key=lambda x: x['score'], reverse=True)
    exploited = sorted(exploited, key=lambda x: x['score'], reverse=True)
    likely = sorted(likely, key=lambda x: x['score'], reverse=True)

    return {
        "All": allv,
        "Critical": crit,
        "Exploited": exploited,
        "Likely Exploited": likely,
    }

@app.route('/login', methods=['GET','POST'])
def login():
    err=None
    if request.method=='POST':
        u, p = request.form['username'], request.form['password']
        if u in USERS and USERS[u]['password']==p:
            login_user(User(u))
            return redirect(url_for('dashboard'))
        err = 'Invalid credentials'
    return render_template('login.html', error=err)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    sections = cve_sections()
    return render_template('dashboard.html', sections=sections)

@app.route('/cve/<cveid>')
@login_required
def cve_detail(cveid):
    vulns = fetch_vulns()
    v = next((v for v in vulns if v.get('CVE') == cveid), None)
    if not v:
        return jsonify({'error':'Not found'}), 404
    score = max((float(s.get('BaseScore',0)) for s in v.get('CVSSScoreSets') or []), default=0)
    return jsonify({
        "cve": v.get('CVE'),
        "title": v.get('Title',{}).get('Value',''),
        "desc": next((n.get('Value') for n in v.get('Notes') or [] if str(n.get('Type','')).lower()=='description'), ''),
        "remediation": next((r.get('URL') for r in v.get('Remediations') or [] if r.get('URL')), ''),
        "score": score,
        "vector": next((s.get('Vector') for s in v.get('CVSSScoreSets') or [] if float(s.get('BaseScore',0))==score), ''),
        "nvd": f"https://nvd.nist.gov/vuln/detail/{v.get('CVE','')}",
    })

@app.route('/export', methods=['POST'])
@login_required
def export():
    ids = request.form.getlist('selected[]')
    vulns = fetch_vulns()
    chosen = [v for v in vulns if v.get('CVE') in ids]
    si = io.StringIO()s
    w = csv.writer(si)
    w.writerow(['CVE ID','Title','Description','Remediation','CVSS Score','Vector','NVD Link'])
    for v in chosen:
        c = v.get('CVE','')
        t = v.get('Title',{}).get('Value','')
        d = next((n.get('Value') for n in v.get('Notes') or [] if str(n.get('Type','')).lower()=='description'), '')
        r = next((r.get('URL') for r in v.get('Remediations') or [] if r.get('URL')), '')
        score = max((float(s.get('BaseScore',0)) for s in v.get('CVSSScoreSets') or []), default=0)
        vector = next((s.get('Vector') for s in v.get('CVSSScoreSets') or [] if float(s.get('BaseScore',0))==score), '')
        nvd = f"https://nvd.nist.gov/vuln/detail/{c}"
        w.writerow([c, t, d, r, score, vector, nvd])
    output = si.getvalue()
    return (output, 200, {'Content-Disposition':'attachment;filename=selected_cves.csv','Content-Type':'text/csv'})

if __name__ == '__main__':
    app.run(debug=True)
