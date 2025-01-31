#!/bin/bash

# RabbitHole/genPrjR00Tt.sh
# Script to generate the RabbitHole project directory structure and set up the Python virtual environment.

set -e  # Exit immediately if a command exits with a non-zero status.
set -u  # Treat unset variables as an error.

# Constants
EXPECTED_STRUCTURE=(
    "auth/__init__.py"
    "auth/oauth.py"
    "auth/password.py"
    "encryption/__init__.py"
    "encryption/encrypt.py"
    "encryption/decrypt.py"
    "storage/__init__.py"
    "storage/database.py"
    "storage/storage.py"
    "ui/__init__.py"
    "ui/fzfInterface.py"
    "ui/clipboard.py"
    "config/__init__.py"
    "config/configManager.py"
    "log/rabbithole.log"
    "data/"  # Directory only
    "tests/__init__.py"
    "tests/testAuth.py"
    "tests/testEncryption.py"
    "tests/testStorage.py"
    "tests/testUI.py"
    "tests/testIntegration.py"
    "main.py"
    "requirements.txt"
    "README.md"
)
EXPECTED_VENV_NAME="RabbitHole-env"

# Function to print messages with emojis
printInfo() {
    echo -e "🐰 [INFO] $1"
}

printWarning() {
    echo -e "⚠️  [WARNING] $1"
}

printError() {
    echo -e "🚫 [ERROR] $1"
}

printSuccess() {
    echo -e "✅ [SUCCESS] $1"
}

# Function to check if running as root
checkRootPrivileges() {
    if [ "$(id -u)" -eq 0 ]; then
        printError "This script should not be run as root. Please run as a regular user."
        exit 1
    fi
}

# Function to check if the directory is empty aside from the script
checkDirectoryStructure() {
    local currentDir
    currentDir=$(pwd)
    local itemCount
    # Count the number of items excluding the script itself
    itemCount=$(ls -A | grep -v "$(basename "$0")" | wc -l)

    if [ "$itemCount" -eq 0 ]; then
        printInfo "Directory is empty. Proceeding to generate project structure."
    else
        # Check if the existing structure matches the expected structure
        local mismatch=false
        for path in "${EXPECTED_STRUCTURE[@]}"; do
            if [[ "$path" == */ ]]; then
                # It's a directory
                if [ ! -d "$path" ]; then
                    mismatch=true
                    printWarning "Expected directory '$path' not found."
                fi
            else
                # It's a file
                if [ ! -f "$path" ]; then
                    mismatch=true
                    printWarning "Expected file '$path' not found."
                fi
            fi
        done

        if [ "$mismatch" = true ]; then
            printError "Current directory contains unexpected files or directories."
            exit 1
        else
            printInfo "Directory contains the expected project structure. No action needed."
            exit 0
        fi
    fi
}

# Function to create directories and touch files
createProjectStructure() {
    printInfo "🛠️  Creating project directory structure and files..."
    for path in "${EXPECTED_STRUCTURE[@]}"; do
        if [[ "$path" == */ ]]; then
            # It's a directory
            mkdir -p "$path"
            printInfo "📁 Created directory '$path'"
        else
            # It's a file
            mkdir -p "$(dirname "$path")"
            touch "$path"
            printInfo "📄 Created file '$path'"
        fi
    done
    printSuccess "Project structure generated successfully."
}

# Function to check virtual environment
checkVirtualEnv() {
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        currentEnv=$(basename "$VIRTUAL_ENV")
        if [ "$currentEnv" != "$EXPECTED_VENV_NAME" ]; then
            printWarning "A different virtual environment ('$currentEnv') is active. Please deactivate it before running this script."
            exit 1
        else
            printInfo "Expected virtual environment '$EXPECTED_VENV_NAME' is already active."
        fi
    else
        # No virtual environment active
        if [ -d "$EXPECTED_VENV_NAME" ]; then
            # Activate existing env
            source "$EXPECTED_VENV_NAME/bin/activate"
            printSuccess "✅ Activated existing virtual environment '$EXPECTED_VENV_NAME'."
        else
            # Create a new virtual environment
            printInfo "🐰 Creating a new virtual environment '$EXPECTED_VENV_NAME'..."
            python3 -m venv "$EXPECTED_VENV_NAME"
            source "$EXPECTED_VENV_NAME/bin/activate"
            printSuccess "✅ Virtual environment '$EXPECTED_VENV_NAME' created and activated."
        fi
    fi
}

# Function to upgrade pip and install dependencies
upgradeDependencies() {
    printInfo "🔄 Upgrading pip, setuptools, buildtools, and disttools..."
    python -m pip install --upgrade pip setuptools buildtools disttools
    printSuccess "✅ Dependencies upgraded successfully."
}

# Main script execution
main() {
    checkRootPrivileges
    checkDirectoryStructure
    createProjectStructure
    checkVirtualEnv
    upgradeDependencies
    printSuccess "🐰 RabbitHole environment setup complete and activated."
}

main
