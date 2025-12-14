import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables explicitly
load_dotenv()

def test_smtp_connection():
    print("--- 📧 EMAIL DIAGNOSTIC TOOL 📧 ---")
    
    # 1. Check Credentials
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    
    print(f"1. Configuration:")
    print(f"   - Host: {smtp_host}")
    print(f"   - Port: {smtp_port}")
    print(f"   - User: {smtp_user}")
    print(f"   - Pass: {'******' if smtp_pass else 'MISSING ❌'}")
    
    if not smtp_user or not smtp_pass:
        print("\n❌ CRITICAL ERROR: SMTP_USER or SMTP_PASSWORD is missing in .env file!")
        return

    # 2. Try Connection
    print("\n2. Testing Connection...")
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1)  # Show detailed conversation
        server.ehlo()
        server.starttls()
        server.ehlo()
        print("   ✅ Connected to SMTP Server!")
        
        # 3. Try Login
        print("\n3. Testing Login...")
        server.login(smtp_user, smtp_pass)
        print("   ✅ Login Successful!")
        
        # 4. Try Sending
        print("\n4. Sending Test Email...")
        msg = MIMEText("This is a test email from the MatrixLead diagnostic tool.\n\nIf you received this, your email system is working perfectly!")
        msg['Subject'] = "MatrixLead Test Email 🚀"
        msg['From'] = smtp_user
        msg['To'] = smtp_user  # Send to yourself
        
        server.send_message(msg)
        print(f"   ✅ Test email sent to {smtp_user}")
        
        server.quit()
        print("\n🎉 SUMMARY: Email system is FULLY OPERATIONAL!")
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION ERROR: Username or Password incorrect.")
        print("   HINT: If using Gmail, you MUST use an 'App Password', not your login password.")
        print("   HINT: Make sure 2-Factor Authentication is enabled on Google.")
    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {str(e)}")

if __name__ == "__main__":
    test_smtp_connection()
