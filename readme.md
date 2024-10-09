# CommVault Error Email Processor

This repository contains two Python scripts for processing and summarizing CommVault error emails. The scripts work together to extract information from error emails, process them, and send summary reports.

## Scripts

### 1. Text to XML Converter (`main_przerabiania_txt_na_xml.py`)

This script processes text files containing CommVault error information and converts them to a structured CSV format.

#### Features:
- Extracts specific information like Detected Time, Job ID, Client, Agent Type, etc.
- Removes duplicate entries based on Job ID
- Moves processed files to a 'done' folder
- Moves skipped files to a 'not_used' folder

#### Usage:
```python
python main_przerabiania_txt_na_xml.py
```

#### Configuration:
- Set `input_folder_path` to the directory containing your text files
- Output CSV file is automatically generated with a timestamp

### 2. Email Table Generator (`main_wysylaj_mailem_tabele.py`)

This script reads unread emails from specified folders, processes them, and sends a summary table via email.

#### Features:
- Connects to an IMAP server to read emails
- Processes emails from specified folders
- Extracts relevant information and formats it into an HTML table
- Sends a summary email with the compiled information

#### Usage:
```python
python main_wysylaj_mailem_tabele.py
```

#### Configuration:
Required variables:
- `glob_EMAIL`: Sender email address
- `glob_EMAIL_FOLDERS`: Tuple of folders to check for emails
- `glob_SENDTO`: Recipient email address(es)
- `glob_PASSWORD`: Email password (stored in separate `secret.py` file)
- `glob_SERVER`: Email server address

## Requirements
- Python 3.x
- Access to an IMAP email server
- Required Python libraries: `email`, `smtplib`, `imaplib`, `csv`

## Setup
1. Clone the repository
2. Create a `secret.py` file with your email password:
```python
password = "your_email_password"
```
3. Adjust the configuration variables in both scripts as needed
4. Ensure you have the required folder structure:
   - Input folder for text files
   - 'done' subfolder
   - 'not_used' subfolder

## Note
This project is specific to CommVault error processing and may need modifications to work with different email formats or error structures.
