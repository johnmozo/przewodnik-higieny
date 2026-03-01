import glob, html5lib
errors = 0
for path in glob.glob('*.html'):
    try:
        parser = html5lib.HTMLParser(strict=True)
        with open(path, encoding='utf-8') as f:
            parser.parse(f.read())
    except Exception as e:
        print(f"{path}: parse error {e}")
        errors += 1
print(f"done, {errors} files with errors")
