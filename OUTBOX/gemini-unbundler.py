import os
import sys

# === CONFIGURATION ===
# Name of the big text file to create or read from
BUNDLE_FILE = "Project_Context.txt"
# Folders to ignore (add more if needed to cut through the "noise")
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build'}
# Files to ignore
IGNORE_FILES = {'.DS_Store', 'package-lock.json', 'yarn.lock', BUNDLE_FILE, 'unbundler.py'}

def bundle(start_path):
    """Reads all files and combines them into one massive text file."""
    print(f"📦 Bundling files from '{start_path}' into '{BUNDLE_FILE}'...")
    
    with open(BUNDLE_FILE, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(start_path):
            # Filter out noisy directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES: continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        # specific format for unbundling later
                        outfile.write(f"\n# === FILE: {rel_path} ===\n")
                        outfile.write(content)
                        outfile.write(f"\n# === END: {rel_path} ===\n")
                        print(f"  + Added: {rel_path}")
                except Exception as e:
                    print(f"  ! Skipped {rel_path} (binary or error)")
    print("✅ Bundle complete!")

def unbundle():
    """Reads the big text file and creates real folders/files."""
    if not os.path.exists(BUNDLE_FILE):
        print(f"❌ Error: Could not find '{BUNDLE_FILE}'")
        return

    print(f"📂 Unbundling '{BUNDLE_FILE}'...")
    with open(BUNDLE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the specific marker we used
    files = content.split('# === FILE: ')
    
    for file_block in files[1:]: # Skip the first empty split
        try:
            # Parse header and content
            header_end = file_block.find(' ===\n')
            filepath = file_block[:header_end].strip()
            
            # Remove the footer marker
            file_content = file_block[header_end+5:].split('# === END:')[0].strip()
            
            # Create directory if needed
            dir_name = os.path.dirname(filepath)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
                
            # Write the file
            with open(filepath, 'w', encoding='utf-8') as out:
                out.write(file_content)
            print(f"  + Created: {filepath}")
            
        except Exception as e:
            print(f"  ! Error processing block: {e}")
            
    print("✅ Unbundle complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "unbundle":
        unbundle()
    else:
        bundle(".")
        print("\n(To reverse this and create files from the text, run: python unbundler.py unbundle)")
