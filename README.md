# RabbitHole

🐰 **RabbitHole**: Dive deep into secure API key management with ease and fun!

RabbitHole is a local API key manager designed to securely store, manage, and access your API keys through an intuitive command-line interface. Seamlessly integrated with your website **Down the Rabbit Hole (DtRH)**, RabbitHole ensures that your secrets remain safe as you navigate the complexities of your projects.

## Features

- **🔒 Secure Authentication:** Password-based authentication with robust hashing (bcrypt).
- **🔐 Encrypted Storage:** Utilizes an encrypted SQLite database (SQLCipher) to store API keys securely.
- **🎯 User-Friendly Interface:** Implements an `fzf`-style fuzzy finder for easy selection of API keys and profiles.
- **🛡️ Secure Clipboard Management:** Copies API keys to the clipboard securely with automatic clearing after a set duration.
- **📜 Detailed Logging:** Maintains rolling log files to monitor application activities without exposing sensitive information.
- **⚙️ Configuration Management:** Automatically manages configuration files and directories with secure defaults based on the host OS.
- **👥 Profile Management:** Allows creation and management of multiple profiles, enabling multiple users on a single local machine.
- **📂 Database Selection and Creation:** Prompts users to select an existing database or create a new one each time, supporting external storage of API keys.
- **🌐 Cross-Platform Support:** Fully compatible with Windows, macOS, Linux, and Android (via Termux).
- **🛠️ Extensible Design:** Modular architecture allows for future enhancements like OAuth integration and GUI development.

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** package manager
- **fzf** installed on your system

#### Installing `fzf`:

- **macOS:**
  
  ```bash
   brew install fzf
  ```

  Linux:

bash
Copy
sudo apt-get install fzf
Windows: Download and install fzf from the official repository.

Android (Termux):

bash
Copy
pkg install fzf
Steps
Clone the Repository:

bash
Copy
git clone https://github.com/yourusername/RabbitHole.git
cd RabbitHole
Run the Project Generation Script:

bash
Copy
./genProject.sh
This script will generate the necessary directory structure, set up the Python virtual environment, and install required dependencies.

Activate the Virtual Environment (if not already activated):

bash
Copy
source RabbitHole-env/bin/activate
Run the Application:

bash
Copy
python main.py
Usage
1. Initial Setup and Profile Creation
On the first run, RabbitHole will prompt you to create a new profile:

bash
Copy
$ python main.py
Terminal Output:

plaintext
Copy
🐰 Welcome to RabbitHole!
🐰 No profiles detected. Please create a new profile.
🐰 Creating a new profile in your RabbitHole.
✨ Enter a unique profile name: WorkAccount
📁 Specify the location for the new database file.
🔍 Enter the directory where you want to create the database: /home/user/Documents/RabbitHole
📄 Enter the name for the new database file (e.g., my_api_keys.db): work_api_keys.db
✅ Database '/home/user/Documents/RabbitHole/work_api_keys.db' created successfully in your RabbitHole.
🔒 Enter your secret password: ************
User authenticated successfully.
🔒 Enter your secret password: ************
🐰 No API keys found. Would you like to add one? (y/n): y
🐰 Enter a label for the API key: GitHub
🔑 Enter the API key: ***************
✅ API key 'GitHub' stored in your RabbitHole successfully.
🔑 API key 'GitHub' pulled from the RabbitHole and copied to clipboard.
Description:

Profile Creation: Since no profiles exist, you're prompted to create one by providing a unique profile name and specifying the location and name for the associated database file.
Database Initialization: RabbitHole writes a magic string to ensure the database's integrity and initializes the encrypted database.
Password Setup and Authentication: You set a password, which is used to derive the encryption key for the database.
API Key Addition: As no API keys are present, you're prompted to add one, which is then encrypted and stored securely in your RabbitHole.
2. Adding Multiple Profiles
To manage multiple users, you can create additional profiles:

bash
Copy
$ python main.py
Terminal Output:

plaintext
Copy
🐰 Welcome to RabbitHole!
🐰 Would you like to select an existing profile? (y/n): y
> WorkAccount
🔒 Enter your secret password: ************
User authenticated successfully.
🔒 Enter your secret password: ************
🐰 Enter a label for the API key: AWS
🔑 Enter the API key: ***************
✅ API key 'AWS' stored in your RabbitHole successfully.
🔑 API key 'AWS' pulled from the RabbitHole and copied to clipboard.
Description:

Profile Selection: If profiles exist, you can choose to select an existing profile using the fzf interface or create a new one.
Adding API Keys: Within the selected profile, you can add multiple API keys, each encrypted and stored in the profile's dedicated database.
3. Selecting and Copying an API Key
With multiple API keys stored within a profile, you can select and copy them as needed:

bash
Copy
$ python main.py
Terminal Output:

plaintext
Copy
🐰 Welcome to RabbitHole!
🐰 Would you like to select an existing profile? (y/n): y
> WorkAccount
🔒 Enter your secret password: ************
User authenticated successfully.
🔒 Enter your secret password: ************
> GitHub
  AWS

🔑 API key 'AWS' pulled from the RabbitHole and copied to clipboard.
Description:

API Key Selection: The fzf interface displays all API key labels associated with the selected profile. You can quickly search and select the desired API key.
Clipboard Operation: The selected API key is decrypted and copied to the clipboard securely, with automatic clearing after the predefined timeout.
4. Clipboard Behavior and Timeout
After copying an API key to the clipboard, it is automatically cleared after 30 seconds to enhance security.

Terminal Output:

plaintext
Copy
🔑 API key 'AWS' pulled from the RabbitHole and copied to clipboard.
After 30 Seconds:

plaintext
Copy
Clipboard cleared after timeout.
Description:

Security Enhancement: This feature ensures that sensitive API keys do not remain in the clipboard longer than necessary, mitigating the risk of unauthorized access or accidental leakage.
5. Handling Errors and Warnings
RabbitHole gracefully handles errors, such as attempting to add an API key with a duplicate label or selecting a non-existent profile.

Scenario: Adding an API Key with an Existing Label

plaintext
Copy
🐰 No API keys found. Would you like to add one? (y/n): y
🐰 Enter a label for the API key: GitHub
🔑 Enter the API key: ***************
🚫 Failed to store API key 'GitHub'. It may already exist.
Log File Entry:

plaintext
Copy
2025-01-31 10:05:00,000 - WARNING - API key with label 'GitHub' already exists.
Description:

Duplicate Label Warning: RabbitHole prevents the addition of duplicate API keys by checking for existing labels, ensuring data integrity and preventing accidental overwrites.

