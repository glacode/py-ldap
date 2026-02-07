import ldap3
from ldap3 import Server, Connection, Tls
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip
import os
from dotenv import load_dotenv
import ssl

# Load environment variables
load_dotenv()
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_USERNAME = os.getenv("LDAP_USERNAME")
LDAP_SEARCH_BASE = os.getenv("LDAP_SEARCH_BASE")
LDAP_PORT = int(os.getenv("LDAP_PORT", "389"))
LDAP_USE_SSL = os.getenv("LDAP_USE_SSL", "False").lower() in ("true", "1", "t")

# Initialize Tkinter root and hide it while asking for password
root = tk.Tk()
root.withdraw()

LDAP_PASSWORD = simpledialog.askstring("LDAP Login", "Enter LDAP password:", show='*')

# Show root window again
root.deiconify()
root.title("LDAP Search")

try:
    ciphers='ALL'
    tls = ldap3.Tls(ciphers=ciphers,validate=ssl.CERT_NONE,version=ssl.PROTOCOL_TLS)
    attributes = ["givenName", "sn", "uid", "cn"]
except Exception as e:
    messagebox.showerror("LDAP Error", str(e))
    exit(1)

if not LDAP_SERVER or not LDAP_USERNAME or not LDAP_SEARCH_BASE:
    messagebox.showerror("Configuration Error", "LDAP_SERVER, LDAP_USERNAME, and LDAP_SEARCH_BASE must be set in the .env file.")
    exit(1)

def search_ldap(firstname, lastname):
    """Search LDAP with a fuzzy match."""
    try:
        ciphers='ALL'
        tls = Tls(ciphers=ciphers,validate=ssl.CERT_NONE,version=ssl.PROTOCOL_TLS)
        serverURL = Server(host=LDAP_SERVER, port=LDAP_PORT, use_ssl=LDAP_USE_SSL, tls=tls)
        conn = Connection(serverURL, LDAP_USERNAME, LDAP_PASSWORD)
        if conn.bind():
            # Forumsys uses 'sn' and 'cn' or 'uid'. 
            # We'll search for sn (lastname) and try to match firstname in cn or givenName
            search_filter = f"(&(objectClass=person)(sn=*{lastname}*)(cn=*{firstname}*))"
            conn.search(LDAP_SEARCH_BASE, search_filter, attributes=attributes)
            print("LDAP connection successful!")
            print("Search result:", conn.entries)
        else:
            print("LDAP connection failed:", conn.result)
        return conn.entries
    except Exception as e:
        messagebox.showerror("LDAP Error", str(e))
        return []

def get_attr_value(entry, attr_names, default=""):
    """Helper to get the first non-empty value from a list of possible attributes."""
    for name in attr_names:
        if hasattr(entry, name):
            attr = getattr(entry, name)
            if attr.value:
                # If multi-valued, take the first one; otherwise return the value as a string
                val = attr.value[0] if isinstance(attr.value, list) else attr.value
                if val: return str(val)
    return default

def on_select(event):
    """Handle double-click on an LDAP entry."""
    selection = listbox.curselection()
    if not selection:
        return
    index = selection[0]
    entry = results[index]
    text_area.delete("1.0", tk.END)
    
    # Extract values using the helper for robust fallback
    username = get_attr_value(entry, ["sAMAccountName", "uid"], "unknown")
    
    # For firstname, try givenName, then fall back to the first part of cn
    firstname = get_attr_value(entry, ["givenName"])
    if not firstname:
        full_name = get_attr_value(entry, ["cn"])
        firstname = full_name.split()[0] if full_name else ""
        
    lastname = get_attr_value(entry, ["sn"])
    info = get_attr_value(entry, ["info", "description"])

    formatted_text = (
        f'username := "{username}"\n'
        f'firstname := StrUpper("{firstname}")\n'
        f'lastname := StrUpper("{lastname}")\n'
        f'info := "{info}"'
    )
    text_area.insert(tk.END, formatted_text)
    pyperclip.copy(formatted_text)
    messagebox.showinfo("Copied", "Text copied to clipboard.")

def on_search():
    """Perform LDAP search and populate the listbox."""
    global results
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    if not firstname or not lastname:
        messagebox.showwarning("Input Required", "Please enter both First Name and Last Name.")
        return
    results = search_ldap(firstname, lastname)
    listbox.delete(0, tk.END)
    for entry in results:
        display_name = f"{getattr(entry, 'cn', entry.sn)} ({getattr(entry, 'uid', '')})"
        listbox.insert(tk.END, display_name)

tk.Label(root, text="First Name:").grid(row=0, column=0)
firstname_entry = tk.Entry(root)
firstname_entry.grid(row=0, column=1)

tk.Label(root, text="Last Name:").grid(row=1, column=0)
lastname_entry = tk.Entry(root)
lastname_entry.grid(row=1, column=1)

tk.Button(root, text="Search", command=on_search).grid(row=2, columnspan=2)

listbox = tk.Listbox(root)
listbox.grid(row=3, columnspan=2, sticky="nsew")
listbox.bind("<Double-Button-1>", on_select)

text_area = tk.Text(root, height=5, width=50)
text_area.grid(row=4, columnspan=2)

try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Unexpected Error", str(e))
    input("Press Enter to exit...")
