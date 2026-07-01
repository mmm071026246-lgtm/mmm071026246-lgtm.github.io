import os
import re
import json
from pathlib import Path
root = Path('.')
out = root / 'report_outputs'
out.mkdir(exist_ok=True)
broken = []
duplicates = []
phrase_duplicates = []
canon_mismatch = []
phrases = ['As you follow this guidance','These symptoms can indicate']
for p in root.rglob('*.html'):
    rel = str(p.relative_to(root)).replace('\\','/')
    try:
        raw = p.read_text(encoding='utf-8')
    except Exception:
        raw = p.read_text(encoding='utf-8',errors='replace')
    # copyright checks
    c_matches = []
    if re.search(r'©\s*fish', raw): c_matches.append('© fish')
    if re.search(r'©\s*\.', raw): c_matches.append('© .')
    if re.search(r'Pet Calculators\s*©\s*(?:$|[^A-Za-z0-9])', raw): c_matches.append('Pet Calculators © (blank/invalid)')
    if c_matches:
        broken.append({'file': rel, 'matches': ', '.join(c_matches)})
    # duplicate paragraphs
    paras = [re.sub(r'\s+',' ',s).strip() for s in re.split(r"\r?\n\s*\r?\n", raw) if len(s.strip())>60]
    counts = {}
    for para in paras:
        counts[para] = counts.get(para,0)+1
    dups = [ {'count':c, 'excerpt': para[:200]} for para,c in counts.items() if c>=2 ]
    if dups:
        duplicates.append({'file': rel, 'repeats': dups})
    # phrase duplicates
    for ph in phrases:
        cnt = len(re.findall(re.escape(ph), raw))
        if cnt>1:
            phrase_duplicates.append({'file': rel, 'phrase': ph, 'count': cnt})
    # canonical
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', raw, flags=re.I)
    if m:
        href = m.group(1).strip()
        expected = 'https://mmm071026246-lgtm.github.io/' + rel
        if href.rstrip('/') != expected.rstrip('/'):
            canon_mismatch.append({'file': rel, 'canonical': href, 'expected': expected})

(out / 'broken_copyright.json').write_text(json.dumps(broken, ensure_ascii=False, indent=2), encoding='utf-8')
(out / 'duplicate_paragraphs.json').write_text(json.dumps(duplicates, ensure_ascii=False, indent=2), encoding='utf-8')
(out / 'phrase_duplicates.json').write_text(json.dumps(phrase_duplicates, ensure_ascii=False, indent=2), encoding='utf-8')
(out / 'canonical_mismatch.json').write_text(json.dumps(canon_mismatch, ensure_ascii=False, indent=2), encoding='utf-8')
print('done')
