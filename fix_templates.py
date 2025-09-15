import os

# Path to your templates folder
TEMPLATES_DIR = "./store/templates/store"  # adjust if different

for root, dirs, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remove {% load currency_filters %}
            content = content.replace("{% load currency_filters %}", "")
            
            # Remove |to_usd from all occurrences
            content = content.replace("|to_usd", "")
            
            # Write back the cleaned template
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Updated {filepath}")
