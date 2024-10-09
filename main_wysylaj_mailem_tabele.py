import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import imaplib
import re
import csv
import time
from datetime import datetime

# hasło z innego pliku
import secret as secret

# od kogo ma byc wysłany email i w jakiej skrzynce szukać maili
glob_EMAIL = 'mateusz.dziezok@coig.pl'
#foldery gdzie szukać maili
glob_EMAIL_FOLDERS = ('CommVault/Errors','CommVault/Failed')
# do kogo wysłać maila
glob_SENDTO = "mateusz.dziezok@coig.pl,mariusz.murawski@coig.pl"
# tutaj podać hasło
glob_PASSWORD = secret.password
# serwer poczty
glob_SERVER = 'mx.coig.pl'

unique_first_items = []

# słowa kluczowe jakie dzieli na kolumny
def extract_lines_from_list(xlist):
    return [line.strip() for line in xlist
        if 'Detected Time:' in line
        or 'Job ID:' in line
        or 'Client:' in line
        or 'Storage Policy Name:' in line
        or 'Copy Name:' in line
        or 'Agent Type:' in line
        or 'Backup Set:' in line
        or 'Subclient:' in line
        or 'Failure Reason:' in line
        ]


#CLEANR = re.compile('<.*?>') 
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
TAG_RE = re.compile(r'<[^>]+>')

def cleanhtml(raw_html):
    return re.sub(TAG_RE, '', raw_html)

def list_without_empty_lines(text):
    lines = text.split('\n')
    list_of_lines = []
    for line in lines:
        if line.strip():
            #print(line)
            list_of_lines.append(line)
    return list_of_lines

'''
def mail_content_to_csv(csv_writer,mail_content):
    content_of_email = list_without_empty_lines(cleanhtml(mail_content))
    print(content_of_email)

    extracted_data = extract_lines_from_list(content_of_email)
    extracted_data = [item.split(':', 1)[-1].strip() for item in extracted_data]

    print("data po ekstakrcji")
    print(extracted_data)

    try:
        Job_ID = extracted_data[1] if extracted_data else None
        if Job_ID not in unique_first_items:
            unique_first_items.append(Job_ID)
            csv_writer.writerow(extracted_data)
    except:
        Job_ID = 000
        csv_writer.writerow(extracted_data)
'''  
def list_to_html_row(data_list):
    html_row = "<tr>\n"
    for item in data_list:
        html_row += f"  <td>{item}</td>\n"
    html_row += "</tr>"
    return html_row

def mail_content_to_string(mail_content):
    content_of_email = list_without_empty_lines(cleanhtml(mail_content))
    #print(content_of_email)

    extracted_data = extract_lines_from_list(content_of_email)
    extracted_data = [item.split(':', 1)[-1].strip() for item in extracted_data]

    print("data po ekstakrcji")
    print(extracted_data)
    return list_to_html_row(extracted_data)

def send_email(conent):

    # Create the email content
    msg = MIMEMultipart("alternative")

    now = datetime.now() # current date and time
    msg['Subject'] = 'Podsumowanie Failed i Errors BETA - ' + now.strftime("%m/%d/%Y")
    msg['From'] = glob_EMAIL
    msg['To'] = glob_SENDTO

    text = "Podsumowanie Failed i Errors BETA"
    html = conent

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    # Send the email
    try:
        with smtplib.SMTP_SSL(glob_SERVER, 465) as server:
            server.login(glob_EMAIL, glob_PASSWORD)
            server.sendmail(glob_EMAIL, glob_SENDTO, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def read_and_print_errors(EMAIL,PASSWORD,SERVER,email_folder):

    #csv_writer = csv.writer(csv_file)
   
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select(email_folder)
    #print(mail.list())
    #status, data = mail.search(None, 'ALL')
    #exit()
    status, data = mail.search(None, 'UNSEEN')
    mail_ids = []

    #print(data)

    if(data == [None]):
        return 0

    for block in data:
        mail_ids += block.split()

    string_inside_of_email = " "

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            mail_content = part.get_payload(decode=True)
                            if mail_content is not None:
                                mail_content = mail_content.decode(errors='replace')
                            break
                else:
                    mail_content = message.get_payload(decode=True)
                    if mail_content is not None:
                        mail_content = mail_content.decode(errors='replace')


                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                #print(f'Content: {cleanhtml(mail_content)}')
                string_inside_of_email = string_inside_of_email+mail_content_to_string(mail_content)

    ## after extracting send email:
    string_inside_of_email = string_inside_of_email
    print(string_inside_of_email)    
    #send_email(string_inside_of_email)
    return(string_inside_of_email)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    email_folders = glob_EMAIL_FOLDERS
    #output_csv = "file"+datetime.today().strftime('%Y-%m-%d---')+".csv"
    email_string = ""
    for folder in email_folders:
        email_string = email_string + str(read_and_print_errors(glob_EMAIL,glob_PASSWORD,glob_SERVER,folder))
    send_email('<table border="1">'+email_string+"</table>")