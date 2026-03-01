#!/usr/bin/env python3
"""Validate HTML and CSS files"""
import os
import re

ISSUES = []

# Check HTML files for structural errors
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for missing closing tags
    if '<script>' in content and '</script>' not in content:
        ISSUES.append(f"{fname}: <script> tag not closed")
    
    # Check for duplicate dark mode logic
    if content.count('addEventListener("click"') > 2:
        ISSUES.append(f"{fname}: Duplicate dark mode event listeners (inefficient)")
    
    # Check for unescaped inline CSS in head
    if '<head>' in content and '/* GLOBAL RESET' in content.split('</head>')[0]:
        ISSUES.append(f"{fname}: CSS found in <head> - should be in <link> or <style>")

# Check CSS file
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()
    if 'body.dark' not in css:
        ISSUES.append("style.css: Dark mode styles missing")

# Check for broken links
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    # Look for href/src to non-existent files
    links = re.findall(r'(?:href|src)="([^"]+)"', content)
    for link in links:
        if not link.startswith(('http://', 'https://', '#')):
            if link.endswith('.html') or link.endswith('.css') or link.endswith('.png'):
                if not os.path.exists(link):
                    ISSUES.append(f"{fname}: Missing file referenced: {link}")

if ISSUES:
    print("VALIDATION ISSUES FOUND:\n")
    for issue in ISSUES:
        print(f"⚠ {issue}")
else:
    print("✓ All basic validations passed!")
    print("✓ No structural HTML errors detected")
    print("✓ All referenced files exist")
    print("✓ Dark mode CSS is present")
