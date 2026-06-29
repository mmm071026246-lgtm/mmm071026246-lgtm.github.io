from pathlib import Path

root = Path(r'c:\Users\com\Desktop\테스트프로\mmm071026246-lgtm.github.io\dog-blog\puppy')
files = sorted([p.name for p in root.iterdir() if p.is_file() and p.name != 'index.html' and p.suffix.lower() == '.html'])


def title_from_filename(name: str) -> str:
    base = name[:-5] if name.endswith('.html') else name
    words = base.split('-')
    result = []
    small = {'a', 'an', 'and', 'or', 'to', 'of', 'for', 'in', 'on', 'at', 'by', 'with', 'your', 'you', 'my', 'is', 'it', 'if', 'do', 'does', 'how', 'what', 'why', 'when', 'can', 'should', 'be', 'the', 'from', 'into', 'up', 'out', 'their', 'while'}
    for word in words:
        if word.lower() in small:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    return ' '.join(result)

sections = [
    ('New Puppy Essentials', ['new', 'checklist', 'buy', 'prepare', 'home', 'first', 'settle', 'supply', 'essential', 'bring', 'welcome']),
    ('Growth & Development', ['growth', 'development', 'grow', 'milestones', 'teeth', 'eyes', 'stop', 'size', 'large', 'small', 'breed', 'baby']),
    ('Feeding & Nutrition', ['feed', 'food', 'water', 'eat', 'nutrition', 'diet', 'portion', 'calorie', 'meal', 'drinking', 'hungry']),
    ('Training & Behavior', ['train', 'behavior', 'socialization', 'introduce', 'separation', 'jump', 'bite', 'bark', 'crate', 'leash', 'potty', 'command', 'behaved', 'chew', 'chewing', 'mistakes']),
    ('Sleep, Routine & Daily Care', ['sleep', 'routine', 'nap', 'night', 'day', 'schedule', 'settle', 'daily', 'care']),
    ('Health & Wellness', ['health', 'vaccin', 'deworm', 'fever', 'sick', 'diarrhea', 'vomiting', 'healthy', 'vet', 'illness', 'common']),
    ('Grooming & Comfort', ['groom', 'bath', 'brush', 'ear', 'paw', 'nail', 'teething', 'shedding', 'coat', 'mats', 'tooth']),
    ('Play, Exercise & Enrichment', ['play', 'exercise', 'toy', 'game', 'walk', 'travel', 'entertained', 'outdoor', 'indoor', 'enrichment', 'active']),
    ('Budget & Planning', ['budget', 'cost', 'spend', 'expense', 'year']),
]

section_map = {name: [] for name, _ in sections}
section_map['Common Questions & Miscellaneous'] = []

for file_name in files:
    lower = file_name.lower()
    placed = False
    for sec_name, keywords in sections:
        if any(keyword in lower for keyword in keywords):
            section_map[sec_name].append(file_name)
            placed = True
            break
    if not placed:
        section_map['Common Questions & Miscellaneous'].append(file_name)

for items in section_map.values():
    items.sort()

html_sections = []
for sec_name in [name for name, _ in sections] + ['Common Questions & Miscellaneous']:
    items = section_map[sec_name]
    if not items:
        continue
    html_sections.append(f"<section class='section'><h2>{sec_name}</h2><div class='grid'>")
    for file_name in items:
        html_sections.append(f"<div class='card'><a href='{file_name}'>{title_from_filename(file_name)}</a><small>{file_name}</small></div>")
    html_sections.append('</div></section>')

html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Puppy Guides | Pet Calculators</title>
<meta name='description' content='Browse puppy guide articles grouped by topic, from first-day prep to growth, feeding, training, health, grooming, and exercise.'>
<meta name='robots' content='index,follow'>
<link rel='canonical' href='https://mmm071026246-lgtm.github.io/dog-blog/puppy/'>
<style>
body{{font-family:Arial,sans-serif;max-width:1200px;margin:auto;padding:20px;background:#f8f9fa;line-height:1.6;color:#222;}}
a{{color:#2563eb;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.hero{{text-align:center;padding:40px 20px;}}
.hero h1{{font-size:38px;margin-bottom:15px;}}
.hero p{{max-width:840px;margin:auto;color:#666;}}
.section{{background:white;padding:25px;margin:25px 0;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.05);}}
.section h2{{margin-bottom:18px;font-size:22px;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;}}
.card{{background:#fafafa;border:1px solid #eef2f7;padding:12px 14px;border-radius:10px;transition:all .2s;}}
.card:hover{{background:#f0f4f8;border-color:#d0dce6;}}
.card a{{display:block;font-weight:600;margin-bottom:4px;}}
.card small{{display:block;color:#6b7280;font-size:12px;}}
.search-box{{max-width:720px;margin:24px auto 10px;display:flex;gap:10px;}}
.search-box input{{flex:1;padding:14px 16px;border:1px solid #ccc;border-radius:10px;font-size:16px;outline:none;}}
.search-box input:focus{{border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,.12);}}
.search-info{{margin:12px auto 0;max-width:720px;color:#555;font-size:0.95rem;}}
footer{{text-align:center;margin-top:50px;padding-top:20px;border-top:1px solid #ddd;color:#666;}}
@media(max-width:768px){{.hero h1{{font-size:32px;}}}}
</style>
</head>
<body>
<a href='../index.html'>← Dog Blog</a>
<div class='hero'>
<h1>Puppy Guides</h1>
<p>Browse puppy articles grouped by topic, from first-day prep and growth to feeding, training, health, grooming, and exercise.</p>
</div>
<div class='search-box'>
<input id='puppySearch' type='search' placeholder='Search puppy guides...' aria-label='Search puppy guides'>
</div>
<p class='search-info' id='searchCount'></p>
{'\n'.join(html_sections)}
<footer>
<p>Pet Calculators © 2026. All rights reserved.</p>
<p><a href='../index.html'>Dog Blog Home</a> | <a href='../../index.html'>Site Home</a></p>
</footer>
<script>
const searchInput = document.getElementById('puppySearch');
const status = document.getElementById('searchCount');
const sections = Array.from(document.querySelectorAll('.section'));
const cards = Array.from(document.querySelectorAll('.card'));

const updateCount = () => {{
  const query = searchInput.value.trim().toLowerCase();
  let visibleCount = 0;
  sections.forEach((section) => {{
    let sectionVisibleCount = 0;
    section.querySelectorAll('.card').forEach((card) => {{
      const title = card.textContent.toLowerCase();
      const isMatch = title.includes(query);
      card.style.display = isMatch ? '' : 'none';
      if (isMatch) sectionVisibleCount += 1;
    }});
    section.style.display = sectionVisibleCount > 0 ? '' : 'none';
    visibleCount += sectionVisibleCount;
  }});
  status.textContent = query ? `${{visibleCount}} articles found.` : `${{visibleCount}} articles available.`;
}};

searchInput.addEventListener('input', updateCount);
updateCount();
</script>
</body>
</html>
"""

(root / 'index.html').write_text(html, encoding='utf-8')
print(f'updated {len(files)} puppy article links into categorized sections')
