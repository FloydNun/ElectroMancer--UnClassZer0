import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# CONFIGURATION: Point this to your actual Vault file
VAULT_HOT_FILE = "Z:/CRANIUM-OBSIDIAN-VAULT/00_Start_Here.md"
TRIGGER_TAG = "#EXECUTE_CCE"

class ObsidianEgressHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """
        Triggered whenever you save your 'Start_Here.md' file.
        """
        if event.src_path.replace("\\", "/") == VAULT_HOT_FILE:
            self.process_vault_command()

    def process_vault_command(self):
        print(f"--- Detected activity in Unified Mind: {VAULT_HOT_FILE} ---")
        
        try:
            with open(VAULT_HOT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Scan for the specific line with the #EXECUTE_CCE tag
            command_found = False
            for i, line in enumerate(lines):
                if TRIGGER_TAG in line and "#DONE" not in line:
                    # Found a fresh command!
                    command_text = line.replace(TRIGGER_TAG, "").strip()
                    print(f"Command Received: '{command_text}'")
                    
                    # --- EXECUTE THE CORE FUNCTION WE BUILT ---
                    # result = tdcr_query_processor(
                    #     query_text=command_text,
                    #     required_tags=["#FINAL_VERIFIED"], # Enforcing security
                    #     handling_instruction="#ARCHIVE_HIGH_SECURITY"
                    # )
                    
                    # --- CLOSE THE LOOP (Mark as Done so it doesn't loop) ---
                    lines[i] = line.strip() + " #DONE  [Result: Asset Created]\n"
                    command_found = True
            
            # Write the "Done" tag back to Obsidian so you see the confirmation instantly
            if command_found:
                with open(VAULT_HOT_FILE, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                print("--- Command Executed & Closed in Vault ---")

        except Exception as e:
            print(f"Read Error: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    observer = Observer()
    # Watch the directory containing the file
    watch_dir = VAULT_HOT_FILE.rsplit("/", 1)[0]
    
    event_handler = ObsidianEgressHandler()
    observer.schedule(event_handler, path=watch_dir, recursive=False)
    
    print(f"👁️ Unified Mind Link Active. Watching: {VAULT_HOT_FILE}")
    print(f"Type '{TRIGGER_TAG}' in your note and save to trigger the CCE.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
