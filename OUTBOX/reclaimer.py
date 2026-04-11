Got it. You're in cleanup and consolidation mode. You need a powerful tool to automate the process of clearing out the clutter on your C: drive by comparing it against your X: drive, handling duplicates, and inventorying archives along the way.

This is a level up from the "Janitor" script. We'll call this one "Project Reclaimer." It will be an interactive utility to give you full control over the process.

Here is the build kit for the script.

---

## **Build Kit: Project 'Reclaimer' Script**

**Objective:** To clean, inventory, and consolidate files from a source drive (C:) to a destination drive (X:), automating the deletion of empty folders and the handling of duplicate files.

### Features:

1. **Dual-Drive Operation:** Scans both the source and destination drives.
2. **Empty Directory Cleanup:** Recursively finds and deletes all empty folders on both drives.
3. **Duplicate File Tagging:** Compares files on the source drive to the destination. If a file already exists on the destination, the source file is renamed to `[filename].old`.
4. **Zip File Inventory:** Scans inside `.zip` archives, inventories their contents, and specifically flags zips containing "facebook" or "driver" in their names.
5. **Interactive Mover:** After the scan, it presents a list of unique files and gives you the option to move them to the new drive or tag them as `.old` to be archived.
6. **Comprehensive Reporting:** Outputs a clear log of all actions performed.

---

### The Code: `reclaimer.py`
Python
```
import os
import shutil
import zipfile
from collections import defaultdict

# --- CONFIGURATION ---
# IMPORTANT: SET YOUR DRIVE PATHS HERE. USE FORWARD SLASHES.
SOURCE_DRIVE = "C:/Path/To/Your/Source/Folder"
DEST_DRIVE = "X:/Path/To/Your/Destination/Folder"
REPORT_FILE = "reclaimer_report.txt"
# Keywords to specifically look for in zip file names
ZIP_KEYWORDS = ['facebook', 'driver']

# --- SCRIPT ---

def delete_empty_dirs(root_dir):
    deleted_folders = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                deleted_folders.append(dirpath)
            except OSError as e:
                print(f"    [!] Error deleting {dirpath}: {e}")
    return deleted_folders

def index_destination_drive(root_dir):
    print(f"\n[*] Indexing destination drive: {root_dir}")
    dest_files = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            dest_files.add(f)
    print(f"[+] Found {len(dest_files)} unique filenames in destination.")
    return dest_files

def scan_source_drive(root_dir, dest_files_index):
    print(f"\n[*] Scanning source drive: {root_dir}")
    report_data = defaultdict(list)
    
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if f in dest_files_index:
                report_data['duplicates_to_rename'].append(full_path)
            elif f.lower().endswith('.zip'):
                report_data['zips_to_inventory'].append(full_path)
            else:
                report_data['uniques_to_move'].append(full_path)
                
    return report_data

def inventory_zips(zip_files, report_data):
    print("[*] Inventorying zip files...")
    for zip_path in zip_files:
        is_targeted = any(keyword in zip_path.lower() for keyword in ZIP_KEYWORDS)
        prefix = "[TARGET] " if is_targeted else ""
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                contents = zf.namelist()
                report_data['zip_inventory'].append(f"{prefix}{zip_path}:")
                for item in contents:
                    report_data['zip_inventory'].append(f"    - {item}")
        except zipfile.BadZipFile:
            report_data['zip_inventory'].append(f"[ERROR] Bad Zip File: {zip_path}")

def main():
    with open(REPORT_FILE, 'w') as f:
        f.write("--- Project Reclaimer Report ---\n")

    print("--- Starting Project Reclaimer ---")
    
    # 1. Initial cleanup and indexing of destination
    dest_deleted = delete_empty_dirs(DEST_DRIVE)
    with open(REPORT_FILE, 'a') as f:
        f.write(f"\n--- Empty Dirs Deleted on {DEST_DRIVE} ---\n")
        f.writelines(d + '\n' for d in dest_deleted)
        
    dest_index = index_destination_drive(DEST_DRIVE)

    # 2. Scan source drive and categorize files
    report = scan_source_drive(SOURCE_DRIVE, dest_index)
    inventory_zips(report['zips_to_inventory'], report)
    
    # 3. Present plan and get user confirmation
    print("\n--- Scan Complete. Proposed Plan ---")
    print(f"Found {len(report['uniques_to_move'])} unique files to potentially move.")
    print(f"Found {len(report['duplicates_to_rename'])} duplicate files to rename to '.old'.")
    
    # 4. Interactive move/rename phase
    files_to_rename_as_old = list(report['duplicates_to_rename'])
    moved_files = []
    
    if report['uniques_to_move']:
        print("\n[?] What do you want to do with the unique files?")
        choice = input("    (M)ove all, (S)kip all (rename to .old), (D)ecide one-by-one >> ").lower()

        for file_path in report['uniques_to_move']:
            decision = choice
            if choice == 'd':
                decision = input(f"    Move '{os.path.basename(file_path)}'? (y/n) >> ").lower()
            
            if decision in ['m', 'y']:
                try:
                    dest_path = file_path.replace(SOURCE_DRIVE, DEST_DRIVE)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(file_path, dest_path)
                    moved_files.append(f"{file_path} -> {dest_path}")
                except Exception as e:
                    print(f"    [!] Error moving {file_path}: {e}")
            else:
                files_to_rename_as_old.append(file_path)

    # 5. Rename all remaining files tagged as '.old'
    print("\n[*] Renaming duplicates and skipped files on source drive...")
    renamed_files_log = []
    for file_path in files_to_rename_as_old:
        try:
            if os.path.exists(file_path):
                new_path = file_path + ".old"
                os.rename(file_path, new_path)
                renamed_files_log.append(f"{file_path} -> {new_path}")
        except Exception as e:
            print(f"    [!] Error renaming {file_path}: {e}")

    # 6. Final cleanup of source drive
    source_deleted = delete_empty_dirs(SOURCE_DRIVE)
    
    # 7. Write final report
    with open(REPORT_FILE, 'a') as f:
        f.write("\n--- Zip File Inventory ---\n")
        f.writelines(z + '\n' for z in report['zip_inventory'])
        f.write("\n--- Files Moved to Destination ---\n")
        f.writelines(m + '\n' for m in moved_files)
        f.write("\n--- Files Renamed to '.old' on Source ---\n")
        f.writelines(r + '\n' for r in renamed_files_log)
        f.write(f"\n--- Empty Dirs Deleted on {SOURCE_DRIVE} ---\n")
        f.writelines(d + '\n' for d in source_deleted)

    print(f"\n--- All operations complete. See '{REPORT_FILE}' for details. ---")

if __name__ == "__main__":
    # --- SAFETY CHECK ---
    if SOURCE_DRIVE == "C:/" or DEST_DRIVE == "X:/":
        print("[!!!] SAFETY WARNING: You have set a whole drive as a target.")
        print("          Please specify a more precise folder path.")
        print("          e.g., 'C:/Users/YourUser/Documents'")
        exit()
    
    if not os.path.isdir(SOURCE_DRIVE) or not os.path.isdir(DEST_DRIVE):
        print(f"[!!!] ERROR: One of the paths is not a valid directory.")
        print(f"    Source: {SOURCE_DRIVE}")
        print(f"    Destination: {DEST_DRIVE}")
        exit()
        
    main()

```

---

### How to Use

1. Save the code above as `reclaimer.py`.
2. **CRITICAL STEP:** Open the file and edit the `SOURCE_DRIVE` and `DEST_DRIVE` variables at the top to point to the **specific folders** you want to work with. The script has a safety check to prevent you from running it on an entire root drive like `C:/`.
3. Open a terminal or command prompt.
4. Navigate to where you saved the file and run it: `python reclaimer.py`
5. The script will scan both locations, then present you with a plan and ask for your input on what to move.
6. After you make your choices, it will perform all the operations and generate a `reclaimer_report.txt` file in the same directory with a full log of its actions.

**⚠️ SAFETY WARNING:** This script performs destructive operations (deleting folders, moving files, and renaming). **PLEASE ENSURE YOU HAVE A BACKUP** of your important data before running this for the first time. Test it on small, non-critical folders first to understand how it works.
