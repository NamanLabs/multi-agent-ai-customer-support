import os

# Jin folders ko skip karna hai (jaise virtual environment aur caches)
IGNORE_DIRS = {'__pycache__', 'multiagent_venv', '.git', '.next', 'node_modules'}
IGNORE_FILES = {'helper_bundle.py', 'project_structure.txt', 'project_content.txt'}
VALID_EXTENSIONS = {'.py', '.json', '.md'} # Aap chahein toh aur extensions add kar sakte hain

output_file_path = "project_content.txt"

with open(output_file_path, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        # Ignore list wale folders ko filter out karein
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
                
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            if ext in VALID_EXTENSIONS:
                outfile.write(f"\n{'='*50}\n")
                outfile.write(f"FILE: {file_path}\n")
                outfile.write(f"{'='*50}\n\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Error reading file: {e}]\n")

print(f"Success! Saara code '{output_file_path}' mein save ho gaya hai.")