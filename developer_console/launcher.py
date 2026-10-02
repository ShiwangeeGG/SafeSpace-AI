# launcher.py

# │

# ├── clear_screen()- cears out the screen every time it is runned 

# ├── print_logo()- prints the initial logo

# ├── check_project()- checks the internal project automatically 

# ├── show_menu() - shows all the opts

# ├── execute_choice()- based on the user requests executes the choice, know as routing.

# └── main()- contols the entire process till user exits 

import os
import subprocess
import sys
from pathlib import Path
from time import sleep

BANNER = r"""
  ____            _   ____                       _
 / ___|  ___  ___| |_|  _ \ ___  _ __ ___   ___ | |_
 \___ \ / _ \/ __| __| |_) / _ \| '_ ` _ \ / _ \| __|
  ___) |  __/\__ \ |_|  _ < (_) | | | | | | (_) | |_
 |____/ \___||___/\__|_| \_\___/|_| |_| |_|\___/ \__|

  SafeSpace AI — RAG Development Launcher
"""

ACTIONS = {
    "1": ("test_retriever.py", "Run Retriever tests"),
    "2": ("test_context_builder.py", "Run Context Builder tests"),
    "3": ("test_prompt_builder.py", "Run Prompt Builder tests"),
    "4": ("check_db.py", "Inspect Vector Database"),
    "5": ("chunk_loader.py", "Rebuild chunks"),
    "6": ("embedding_generator.py", "Rebuild embeddings"),
    "7": (None, "Exit")
}


def clear_screen() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def supports_color() -> bool:
    return sys.stdout.isatty()


def color_text(text: str, code: str) -> str:
    if supports_color():
        return f"\033[{code}m{text}\033[0m"
    return text


def print_logo() -> None:
    print(color_text(BANNER, "1;36"))
    print(color_text("Version 1.0 • Author: Piu Ghosh", "33"))
    print(color_text("Directory: " + str(Path.cwd()), "32"))
    print("" + "=" * 60)
    print()


def show_menu() -> str:
    print(color_text("Select an action:", "1;34"))
    for key, (_, title) in ACTIONS.items():
        print(f"  {color_text(key, '1;33')}  {title}")
    print()
    return input(color_text("Choice: ", "1;32")).strip()

def check_files():

    files = {

        "Retriever": "test_retriever.py",

        "Context Builder": "context_builder.py",

        "Prompt Builder": "prompt_builder.py",

        "Generator": "generator.py",

        "Chat": "chat.py"

    }

    status = {}

    for name, file in files.items():

        if os.path.exists(file):

            status[name] = "✅ Ready"

        else:

            status[name] = "⏳ Not Built"

    return status

import os

def check_files():

    files = {

        "Retriever": "test_retriever.py",

        "Context Builder": "context_builder.py",

        "Prompt Builder": "prompt_builder.py",

        "Generator": "generator.py",

        "Chat": "chat.py"

    }

    status = {}

    for name, file in files.items():

        if os.path.exists(file):

            status[name] = "✅ Ready"

        else:

            status[name] = "⏳ Not Built"

    return status

def project_status():

    print("\n📊 PROJECT HEALTH\n")

    print("Knowledge Base      ✅ Ready")

    print("Chunks             ✅ 504 Chunks")

    print("Vector Database    ", check_database())

    file_status = check_files()

    for module, state in file_status.items():

        print(f"{module:<20} {state}")
        
def run_script(script_name: str) -> None:
    script_path = Path(script_name)
    if not script_path.exists():
        print(color_text(f"Error: {script_name} not found.", "1;31"))
        return

    command = [sys.executable, script_name]
    try:
        subprocess.run(command, check=False)
    except KeyboardInterrupt:
        print(color_text("\nExecution interrupted.", "1;31"))


def execute_choice(choice: str) -> bool:
    action = ACTIONS.get(choice)
    if not action:
        print(color_text("Invalid choice. Please select a number from the menu.", "1;31"))
        return True

    script_name, title = action
    if choice == "7":
        print(color_text("\nGoodbye 👋", "1;36"))
        return False

    print(color_text(f"\nRunning: {title}", "1;34"))
    if choice == "6":
        print(color_text("Note: delete vector_db manually if rebuilding from scratch.", "33"))
    run_script(script_name)
    return True


def pause() -> None:
    try:
        input(color_text("\nPress ENTER to return to the menu...", "1;32"))
    except KeyboardInterrupt:
        print()


def main() -> None:
    while True:
        clear_screen()
        print_logo()
        choice = show_menu()
        should_continue = execute_choice(choice)
        if not should_continue:
            break
        pause()


if __name__ == "__main__":
    main()
