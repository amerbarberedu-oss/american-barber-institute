#!/usr/bin/env python3
"""Deploy this static site to Vercel via the REST API (no CLI/Node needed).

Usage: VERCEL_TOKEN=... [TEAM_ID=...] python3 src/deploy_vercel.py
Uploads every tracked site file, then creates a production deployment.
"""
import hashlib, json, os, subprocess, sys, time, urllib.request, urllib.error

TOKEN = os.environ.get('VERCEL_TOKEN')
TEAM = os.environ.get('TEAM_ID', '')
if not TOKEN:
    sys.exit('VERCEL_TOKEN env var required')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = 'abi-website'
API = 'https://api.vercel.com'
Q = ('?teamId=' + TEAM) if TEAM else ''


def req(method, url, data=None, headers=None, raw=False):
    h = {'Authorization': 'Bearer ' + TOKEN}
    if headers:
        h.update(headers)
    if data is not None and not raw:
        data = json.dumps(data).encode()
        h['Content-Type'] = 'application/json'
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read() or b'{}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        return e.code, json.loads(body) if body.startswith('{') else {'raw': body}


# 1. collect git-tracked files (exclude dev/build sources not needed to serve)
tracked = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).split()
SKIP_PREFIX = ('src/', '.claude/', '.gitignore')
# Don't serve source, docs, or markdown on the live site.
files = [f for f in tracked if not f.startswith(SKIP_PREFIX) and not f.endswith('.md')]
print(f'{len(files)} files to upload')

# 2. upload each file blob (content-addressed by sha1)
manifest = []
up = cached = 0
for i, path in enumerate(files):
    blob = open(os.path.join(ROOT, path), 'rb').read()
    sha = hashlib.sha1(blob).hexdigest()
    manifest.append({'file': path, 'sha': sha, 'size': len(blob)})
    for attempt in range(4):
        code, _ = req('POST', f'{API}/v2/files{Q}', data=blob, raw=True, headers={
            'x-vercel-digest': sha,
            'Content-Type': 'application/octet-stream',
        })
        if code in (200, 201):
            up += 1
            break
        if code == 409:  # already uploaded
            cached += 1
            break
        time.sleep(2 * (attempt + 1))
    else:
        sys.exit(f'upload failed for {path} (HTTP {code})')
    if (i + 1) % 50 == 0:
        print(f'  {i+1}/{len(files)} uploaded')

print(f'uploads done (new={up} cached={cached})')

# 3. create production deployment
code, dep = req('POST', f'{API}/v13/deployments{Q}', data={
    'name': PROJECT,
    'project': PROJECT,
    'target': 'production',
    'files': manifest,
    'projectSettings': {'framework': None},
})
if code not in (200, 201):
    sys.exit(f'deployment create failed: HTTP {code} {json.dumps(dep)[:400]}')
dep_id = dep['id']
print('deployment created:', dep.get('url'))

# 4. poll until ready
for _ in range(60):
    code, d = req('GET', f'{API}/v13/deployments/{dep_id}{Q}')
    state = d.get('readyState') or d.get('status')
    print('  state:', state)
    if state == 'READY':
        print('PRODUCTION URL: https://' + d['url'])
        aliases = d.get('alias') or []
        for a in aliases:
            print('ALIAS: https://' + a)
        sys.exit(0)
    if state in ('ERROR', 'CANCELED'):
        sys.exit('deployment failed: ' + json.dumps(d)[:400])
    time.sleep(5)
sys.exit('timed out waiting for deployment')
