#!/usr/bin/env python3
import datetime
import requests
import pandas as pd

API_VERSION = 'v3.0'
BASE_URL    = f'https://api.msrc.microsoft.com/cvrf/{API_VERSION}/cvrf/' # ie 2025-Jul
HEADERS     = {'Accept': 'application/json'}
THREAT_EXP  = 1

def current_ym():
    return datetime.datetime.now().strftime("%Y-%b")

def max_score_vector(v):
    best = -1.0
    vec  = ''
    for s in v.get('CVSSScoreSets') or []:
        try:
            bs = float(s.get('BaseScore', 0))
        except:
            continue
        if bs > best:
            best, vec = bs, (s.get('Vector') or '')
    return (best if best >= 0 else 0.0, vec)

def ms_sev(score):
    if score >= 9.0: return 'Critical'
    if score >= 7.0: return 'Important'
    if score >= 4.0: return 'Moderate'
    if score  >  0: return 'Low'
    return ''

def note(v, typ):
    for n in v.get('Notes') or []:
        if not isinstance(n, dict): continue
        t = str(n.get('Type') or n.get('Title') or '').lower()
        if t == typ.lower():
            return (n.get('Value') or '').strip()
    return ''

def flatten_products(v):
    parts = []
    for ps in v.get('ProductStatuses') or []:
        for pid in ps.get('ProductID') or []:
            parts.append(str(pid))
    return "; ".join(parts)

class MSRC:
    def __init__(self, ym):
        r = requests.get(BASE_URL + ym, headers=HEADERS)
        r.raise_for_status()
        d = r.json()
        self.title = d.get('DocumentTitle', {}).get('Value', '')
        self.vulns = d.get('Vulnerability') or []

    def classification(self):
        labels = [
            'Elevation of Privilege', 'Security Feature Bypass',
            'Remote Code Execution', 'Information Disclosure',
            'Denial of Service', 'Spoofing', 'Edge - Chromium'
        ]
        counts = {lbl: 0 for lbl in labels}
        for v in self.vulns:
            seen = set()
            for t in v.get('Threats') or []:
                if t.get('Type') != 0: continue
                desc = t.get('Description', {}).get('Value', '')
                if desc == 'Edge - Chromium' and '11655' in t.get('ProductID', []):
                    seen.add(desc)
                elif desc in counts:
                    seen.add(desc)
            for lbl in seen:
                counts[lbl] += 1
        return pd.DataFrame.from_dict(counts, orient='index', columns=['Count']).rename_axis('Classification')

    def exploited(self):
        rows = []
        for v in self.vulns:
            bs, _ = max_score_vector(v)
            for t in v.get('Threats') or []:
                if t.get('Type') == THREAT_EXP and 'Exploited:Yes' in t.get('Description', {}).get('Value', ''):
                    rows.append({'CVE': v.get('CVE'), 'Score': bs, 'Title': v.get('Title', {}).get('Value')})
                    break
        return pd.DataFrame(rows)

    def high(self, thr=8.0):
        rows = []
        for v in self.vulns:
            bs, _ = max_score_vector(v)
            if bs >= thr:
                rows.append({'CVE': v.get('CVE'), 'Score': bs, 'Title': v.get('Title', {}).get('Value')})
        return pd.DataFrame(rows)

    def likely(self):
        rows = []
        for v in self.vulns:
            for t in v.get('Threats') or []:
                if t.get('Type') == THREAT_EXP and 'exploitation more likely' in t.get('Description', {}).get('Value', '').lower():
                    rows.append({'CVE': v.get('CVE'), 'Title': v.get('Title', {}).get('Value')})
                    break
        return pd.DataFrame(rows)

def main():
    ym = current_ym()
    m  = MSRC(ym)

    df_sum   = pd.DataFrame({
        'Release Title': [m.title],
        'Year-Month':     [ym],
        'Total Vulns':    [len(m.vulns)]
    })
    df_class = m.classification()
    df_wild  = m.exploited()
    df_high  = m.high()
    df_likely= m.likely()

    rows = []
    for v in m.vulns:
        cve    = v.get('CVE','')
        qid    = ''
        title  = v.get('Title',{}).get('Value','')
        desc   = note(v, 'Description')
        bs, vec= max_score_vector(v)
        ms     = ms_sev(bs)
        threats= v.get('Threats') or []
        act    = 'Yes' if any(t.get('Type')==THREAT_EXP and 'Exploited:Yes' in t.get('Description',{}).get('Value','') for t in threats) else 'No'
        pub    = 'Yes' if any(t.get('Type')==THREAT_EXP and 'Public' in t.get('Description',{}).get('Value','') for t in threats) else 'No'
        imp    = flatten_products(v)
        exp_as = note(v, 'ExploitabilityAssessment')
        notes  = "; ".join(
            (n.get('Value') or '').strip()
            for n in v.get('Notes') or []
            if str(n.get('Type') or n.get('Title') or '').lower() not in
               ('description','severity','exploitabilityassessment')
        )
        rows.append({
            'CVE ID': cve, 'QID': qid, 'Title': title,
            'Description': desc, 'MS Severity': ms,
            'Actively Exploited': act, 'Publicly Disclosed': pub,
            'Impacted Product': imp, 'CVSS Score': bs,
            'Vector String': vec, 'Exploitation Assessment': exp_as,
            'Notes': notes
        })
    df_needs = pd.DataFrame(rows, columns=[
        'CVE ID','QID','Title','Description','MS Severity',
        'Actively Exploited','Publicly Disclosed','Impacted Product',
        'CVSS Score','Vector String','Exploitation Assessment','Notes'
    ])

    with pd.ExcelWriter(f"MSRC_{ym}.xlsx", engine='openpyxl') as w:
        df_sum.to_excel(w, 'Summary', index=False)
        df_class.to_excel(w, 'By Classification')
        df_wild.to_excel(w, 'Exploited in Wild', index=False)
        df_high.to_excel(w, 'High Severity (≥8.0)', index=False)
        df_likely.to_excel(w, 'Likely Exploited', index=False)
        df_needs.to_excel(w, 'Needs Patch', index=False)

        df_patch = df_needs[
            (df_needs['MS Severity']=='Critical') |
            (df_needs['Actively Exploited']=='Yes')
        ]
        df_patch = df_patch[
            ~df_patch['Impacted Product'].str.contains('Windows', na=False)
        ]
        df_patch.to_excel(w, 'Patch Now', index=False)

        patch_later = df_needs.loc[df_needs.index.difference(df_patch.index)]
        patch_later.to_excel(w, 'Patch Later', index=False)

        for sheet in w.sheets.values():
            for col in sheet.columns:
                width = max(len(str(cell.value)) for cell in col) + 2
                sheet.column_dimensions[col[0].column_letter].width = width

    print(f"Wrote MSRC_{ym}.xlsx")

if __name__=='__main__':
    main()
