from pathlib import Path
import xml.etree.ElementTree as ET

# Parse existing sitemap
sitemap_path = Path('sitemap.xml')
tree = ET.parse(sitemap_path)
root = tree.getroot()

# Define namespace
ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

# Get all health blog files
health_dir = Path('dog-blog/health')
health_files = sorted([f.name for f in health_dir.glob('*.html') if f.name != 'index.html'])

# Find the position to insert (after the health/index.html entry)
existing_urls = root.findall('sitemap:url', ns) if ns else root.findall('url')
if not existing_urls:
    existing_urls = root.findall('url')

insert_index = -1
for i, url_elem in enumerate(existing_urls):
    loc = url_elem.find('sitemap:loc', ns) if ns else url_elem.find('loc')
    if loc is None:
        loc = url_elem.find('loc')
    if loc is not None and 'dog-blog/health/index.html' in loc.text:
        insert_index = i + 1
        break

# Create new URL entries
base_url = 'https://mmm071026246-lgtm.github.io/'
new_urls = []

for filename in health_files:
    url_elem = ET.Element('url')
    loc_elem = ET.SubElement(url_elem, 'loc')
    loc_elem.text = f'{base_url}dog-blog/health/{filename}'
    new_urls.append(url_elem)

# Insert the new URLs
if insert_index >= 0:
    for i, new_url in enumerate(new_urls):
        root.insert(insert_index + i, new_url)
else:
    # If not found, append to the end
    for new_url in new_urls:
        root.append(new_url)

# Write the updated sitemap
tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)

print(f'✓ Added {len(health_files)} health blog articles to sitemap.xml')
