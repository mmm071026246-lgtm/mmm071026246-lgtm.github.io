import os
import re
from pathlib import Path

def convert_to_title(filename):
    """Convert 'dog-age-calculator.html' to 'Dog Age Calculator'"""
    name = filename.replace('.html', '')
    words = name.split('-')
    return ' '.join(word.capitalize() for word in words)

# Get all HTML files except index.html
health_dir = Path('dog-blog/health')
files = sorted([f.name for f in health_dir.glob('*.html') if f.name != 'index.html'])

# Categories for organization
categories = {
    'Emergency & First Aid': r'emergency|first-aid|heatstroke|poisoning|choking|bloat|trauma|seizure|burn',
    'Skin, Allergy & Coat': r'allergy|dermatitis|rash|itching|folliculitis|seborrheic|skin|hair-loss|coat',
    'Eyes, Ears & Oral Health': r'ear|eye|dental|teeth|mouth|gum|oral|dry-eyes|mites',
    'Parasites & Prevention': r'parasite|flea|tick|worm|deworm|preventive|prevention|heartworm',
    'Joints & Mobility': r'arthritis|joint|hip|cruciate|limping|walking|mobility|pain',
    'Weight & Nutrition': r'weight|obesity|nutrition|calorie|body-condition|supplement',
    'Vaccines & Wellness': r'vaccine|vaccination|wellness|checkup|screening|health-check',
    'Senior Dog Care': r'senior|dementia|hydration|sleep|safety',
}

# Track assigned files
assigned = {f: False for f in files}
sections = []

# Assign files to categories
for category_name, pattern in categories.items():
    items = [f for f in files if not assigned[f] and re.search(pattern, f)]
    if items:
        sections.append((category_name, sorted(items)))
        for item in items:
            assigned[item] = True

# Add unassigned to General Health
unassigned = [f for f in files if not assigned[f]]
if unassigned:
    sections.append(('General Health & Wellness', sorted(unassigned)))

# Build HTML
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dog Health Guides | Pet Calculators</title>
<meta name="description" content="Browse all dog health guides and articles, grouped by topic." />
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="https://mmm071026246-lgtm.github.io/dog-blog/health/">
<style>
body {
  font-family: Arial, sans-serif;
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px 48px;
  color: #1f2937;
  background: #f8fafc;
  line-height: 1.6;
}

a {
  color: #2563eb;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.breadcrumb {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 20px;
}

.hero {
  background: white;
  padding: 28px 24px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.hero h1 {
  font-size: 32px;
  margin: 0 0 10px 0;
}

.hero p {
  margin: 0;
  color: #4b5563;
}

.section {
  background: white;
  padding: 20px 22px;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.section h2 {
  font-size: 22px;
  margin: 0 0 12px 0;
  color: #1f2937;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.card {
  background: #fafafa;
  border: 1px solid #eef2f7;
  padding: 12px 14px;
  border-radius: 10px;
  transition: all 0.2s;
}

.card:hover {
  background: #f0f4f8;
  border-color: #d0dce6;
}

.card a {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
  color: #2563eb;
}

.card small {
  color: #6b7280;
  font-size: 12px;
}

.footer-note {
  margin-top: 30px;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

@media (max-width: 700px) {
  body { padding: 16px; }
  .hero h1 { font-size: 26px; }
}
</style>
</head>
<body>

<nav class="breadcrumb" aria-label="breadcrumb">
<a href="../../index.html">Home</a> › <a href="../index.html">Dog Blog</a> › <span>Health Guides</span>
</nav>

<div class="hero">
<h1>Dog Health Guides</h1>
<p>Browse our complete collection of dog health articles grouped by topic.</p>
</div>
'''

# Add sections
for category_name, items in sections:
    html_content += f'\n<section class="section"><h2>{category_name}</h2>\n<div class="grid">\n'
    for filename in items:
        title = convert_to_title(filename)
        html_content += f'<div class="card"><a href="{filename}">{title}</a><small>{filename}</small></div>\n'
    html_content += '</div>\n</section>\n'

html_content += '''
<footer class="footer-note">
<p>Pet Calculators © . Always consult a licensed veterinarian for personalized medical advice.</p>
</footer>

</body>
</html>
'''

# Write to file
output_path = health_dir / 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'✓ Updated {output_path}')
print(f'✓ Total files indexed: {len(files)}')
print(f'✓ Categories: {len(sections)}')
