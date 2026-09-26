import imaplib
import email
import requests

# Gmail credentials aur webhook URL configure karein
IMAP_SERVER = 'imap.gmail.com'
EMAIL_USER = 'sahilxd892@gmail.com'
EMAIL_PASS = 'cswdmizrirzbdnmf'
WEBHOOK_URL = 'https://my-telegram-bot-production-47a7.up.railway.app/webhook'

def check_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select('inbox')
    
    # Unread emails search karein
    status, messages = mail.search(None, 'UNSEEN')
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Email subject aur sender check karein
        subject = msg['subject']
        if 'Payment Received' in subject:
            # Email body se details parse karein
            # Yeh part apke email format ke hisaab se hoga
            user_id = 'parsed_user_id'
            amount = 'parsed_amount'
            
            # Webhook par data bhejein
            payload = {'user_id': user_id, 'amount': amount}
            requests.post(WEBHOOK_URL, json=payload)
            
    mail.close()
    mail.logout()
