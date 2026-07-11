import glob
import re

for file in glob.glob('*.py'):
    if file == 'fix_urls.py': continue
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
    
    # replace BASE_URL to have /api
    content = re.sub(r'BASE_URL\s*=\s*"http://localhost:8000"', 'BASE_URL = "http://localhost:8000/api"', content)
    
    # replace any f"{BASE_URL}/api/ with f"{BASE_URL}/
    content = content.replace('f"{BASE_URL}/api/', 'f"{BASE_URL}/')
    
    # replace any missing slashes for auth-enhanced
    content = content.replace('f"{BASE_URL}/auth-enhanced', 'f"{BASE_URL}/auth-enhanced')
    
    with open(file, 'w', encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed {file}")
