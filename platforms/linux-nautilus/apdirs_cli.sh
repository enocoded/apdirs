#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Paths
SCRIPT_PATH="$(readlink -f -- "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
VERSION="$(<"$SCRIPT_DIR/../../VERSION")"
BASE_DIR="$HOME/Projects/client-work"
TEMPLATE_DIR="$BASE_DIR/templates"

normalize_input() {
    python3 -c 'import sys; sys.stdout.write(sys.argv[1].strip().lower().replace(" ", "-"))' "$1"
}

echo "==========================================="
echo "   Apdirs - Archviz Project Manager v$VERSION "
echo "==========================================="
echo "Select an action:"
echo "  1) Create a new project"
echo "  2) Add a dated folder to an existing project"
read -p "Choice [1/2]: " CHOICE

if [ "$CHOICE" = "1" ]; then
    # --- MODE 1: CREATE NEW PROJECT ---
    read -p "Client name (e.g., abc-company): " CLIENT_INPUT
    read -p "Project description (e.g., modern-interior): " PROJECT_INPUT

    CLIENT_NAME=$(normalize_input "$CLIENT_INPUT")
    PROJECT_SLUG=$(normalize_input "$PROJECT_INPUT")

    if [ -z "$CLIENT_NAME" ] || [ -z "$PROJECT_SLUG" ]; then
        echo "Error: Client name and project slug cannot be empty."
        exit 1
    fi

    CURRENT_DATE=$(date +%Y-%m-%d)
    PROJECT_FOLDER="${CURRENT_DATE}_${CLIENT_NAME}_${PROJECT_SLUG}"
    FULL_PATH="$BASE_DIR/$PROJECT_FOLDER"

    echo -e "\nCreating project structure at:\n$FULL_PATH\n"

    mkdir -p "$FULL_PATH/01-inputs/${CURRENT_DATE}/drawings"
    mkdir -p "$FULL_PATH/01-inputs/${CURRENT_DATE}/refs"
    mkdir -p "$FULL_PATH/01-inputs/${CURRENT_DATE}/insps"

    mkdir -p "$FULL_PATH/02-production/components"
    mkdir -p "$FULL_PATH/02-production/export"
    mkdir -p "$FULL_PATH/02-production/assets/maps"
    mkdir -p "$FULL_PATH/02-production/assets/meshes"
    mkdir -p "$FULL_PATH/02-production/assets/hdris"
    mkdir -p "$FULL_PATH/02-production/ro"
    mkdir -p "$FULL_PATH/02-production/post"

    mkdir -p "$FULL_PATH/03-deliverables/"

    if [ -f "$TEMPLATE_DIR/brief-template.docx" ]; then
        cp "$TEMPLATE_DIR/brief-template.docx" "$FULL_PATH/01-inputs/${CURRENT_DATE}/${CURRENT_DATE}_${PROJECT_SLUG}_brief.docx"
        echo " -> Copied project brief template."
    fi

    echo -e "\nSuccess! Project initialized and ready."

elif [ "$CHOICE" = "2" ]; then
    # --- MODE 2: ADD DATED FOLDER TO EXISTING PROJECT ---
    echo -e "\n--- Ongoing Projects in client-work ---"
    
    # Use a native bash glob loop; [ -d ] automatically resolves symlinked project folders
    projects=()
    for item in "$BASE_DIR"/*; do
        if [ -d "$item" ]; then
            projects+=("$item")
        fi
    done

    if [ ${#projects[@]} -eq 0 ]; then
        echo "No projects found in $BASE_DIR."
        exit 1
    fi

    for i in "${!projects[@]}"; do
        echo "  $((i+1))) $(basename "${projects[$i]}")"
    done

    read -p "Select project number: " PROJ_CHOICE
    
    if ! [[ "$PROJ_CHOICE" =~ ^[0-9]+$ ]] || [ "$PROJ_CHOICE" -lt 1 ] || [ "$PROJ_CHOICE" -gt "${#projects[@]}" ]; then
        echo "Error: Invalid project selection."
        exit 1
    fi

    SELECTED_PROJECT="${projects[$((PROJ_CHOICE-1))]}"
    echo -e "\nSelected: $(basename "$SELECTED_PROJECT")"

    echo ""
    echo "Where do you want to add the dated folder?"
    echo "  1) 01-inputs"
    echo "  2) 03-deliverables"
    read -p "Target folder [1/2]: " TARGET_CHOICE

    if [ "$TARGET_CHOICE" = "1" ]; then
        TARGET_DIR="$SELECTED_PROJECT/01-inputs"
    elif [ "$TARGET_CHOICE" = "2" ]; then
        TARGET_DIR="$SELECTED_PROJECT/03-deliverables"
    else
        echo "Error: Invalid target folder selection."
        exit 1
    fi

    TODAY=$(date +%Y-%m-%d)
    read -p "Optional folder label (leave blank for just '$TODAY', e.g., 'client-revision'): " LABEL_INPUT
    
    CLEAN_LABEL=$(normalize_input "$LABEL_INPUT")

    if [ -z "$CLEAN_LABEL" ]; then
        NEW_FOLDER_NAME="$TODAY"
    else
        NEW_FOLDER_NAME="${TODAY}_${CLEAN_LABEL}"
    fi

    FINAL_TARGET="$TARGET_DIR/$NEW_FOLDER_NAME"
    mkdir -p "$FINAL_TARGET"

    if [ "$TARGET_CHOICE" = "1" ]; then
        mkdir -p "$FINAL_TARGET/drawings"
        mkdir -p "$FINAL_TARGET/refs"
        mkdir -p "$FINAL_TARGET/insps"
        
        if [ -f "$TEMPLATE_DIR/brief-template.docx" ]; then
            cp "$TEMPLATE_DIR/brief-template.docx" "$FINAL_TARGET/${NEW_FOLDER_NAME}_brief.docx"
            echo " -> Copied project brief template to $NEW_FOLDER_NAME/"
        fi
    fi

    echo -e "\nSuccess! Created dated folder at:\n$FINAL_TARGET"

else
    echo "Invalid choice. Exiting."
    exit 1
fi