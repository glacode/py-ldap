# Python LDAP Search Utility

A GUI-based LDAP search tool designed to streamline user lookups and data extraction. This utility connects to an LDAP directory, allows for fuzzy searching of personnel, and provides a formatted output that is automatically copied to the clipboard for ease of use in other applications.

## Features

- **Intuitive GUI:** Built with `tkinter` for a responsive and native desktop experience.
- **Fuzzy Search:** Implements LDAP filters to search users by first and last name combinations.
- **Secure Authentication:** Prompts for credentials at runtime using masked input fields, ensuring sensitive passwords are never stored in plaintext.
- **Dynamic Configuration:** Utilizes environment variables (`.env`) for flexible deployment across different LDAP environments.
- **Clipboard Integration:** Automatically formats results (e.g., upper-casing names) and copies them to the system clipboard using `pyperclip`.
- **Robust Error Handling:** Includes comprehensive validation for network connections, TLS handshake, and missing configurations.
- **Attribute Fallbacks:** Smart parsing of LDAP attributes (CN, SN, UID, givenName) to ensure data consistency across varying directory schemas.

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **LDAP Protocol:** `ldap3` (A strictly RFC 4510 compliant LDAPv3 client library)
- **GUI Framework:** `tkinter`
- **Configuration:** `python-dotenv`
- **Utilities:** `pyperclip` for clipboard management, `ssl` for secure connections.

## Prerequisites

- Python 3.x
- A virtual environment (recommended)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/py-ldap.git
   cd py-ldap
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have `ldap3`, `python-dotenv`, and `pyperclip` installed.)*

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory based on the following template:

   ```env
   LDAP_SERVER=ldap.forumsys.com
   LDAP_USERNAME=cn=read-only-admin,dc=example,dc=com
   LDAP_SEARCH_BASE=dc=example,dc=com
   LDAP_PORT=389
   LDAP_USE_SSL=False
   ```

## Usage

1. **Run the application:**
   ```bash
   python searchLdapUser.py
   ```
2. **Login:** A dialog will appear asking for your LDAP password.
3. **Search:** Enter a first and last name in the provided fields and click **Search**.
4. **Select & Copy:** Double-click any result in the listbox. The user details will be formatted and copied to your clipboard automatically.

## 🧪 Testing with Forumsys

This project is pre-configured to work with the **[Forumsys Public LDAP Server](https://www.forumsys.com/2022/02/25/online-ldap-test-server/)**, a fantastic free resource for developers to test LDAP integrations.

**Test Credentials for Forumsys:**
- **Server:** `ldap.forumsys.com`
- **Port:** `389`
- **Bind DN:** `cn=read-only-admin,dc=example,dc=com`
- **Password:** `password`
- **Search Base:** `dc=example,dc=com`

*Special thanks to Forumsys for providing this service to the developer community.*

## 📜 License

This project is for demonstration purposes. Feel free to use and modify it as needed. Always ensure you have permission before connecting to private LDAP directories.