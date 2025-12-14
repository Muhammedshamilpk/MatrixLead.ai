# agents/email_service.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging
from typing import Optional

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_service")


class EmailService:
    """
    Email service for sending automated emails to qualified leads.
    Supports both SMTP and Gmail API.
    """
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.from_name = os.getenv("FROM_NAME", "MatrixLead AI")
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str
    ) -> dict:
        """
        Send a plain text email using SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_text: Plain text email body
            
        Returns:
            dict with status and message
        """
        if not self.smtp_user or not self.smtp_password:
            logger.error("SMTP credentials not configured")
            return {
                "status": "error",
                "message": "Email service not configured. Please set SMTP_USER and SMTP_PASSWORD in .env"
            }
        
        try:
            # Create plain text message
            msg = MIMEText(body_text, 'plain')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Connect to SMTP server
            logger.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            
            # Login
            server.login(self.smtp_user, self.smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent successfully to {to_email}")
            return {
                "status": "sent",
                "message": f"Email sent to {to_email}",
                "to": to_email,
                "subject": subject
            }
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed")
            return {
                "status": "error",
                "message": "Email authentication failed. Check SMTP credentials."
            }
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return {
                "status": "error",
                "message": f"SMTP error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}"
            }


def generate_qualified_lead_email(lead_data: dict) -> dict:
    """
    Generate personalized plain text email content for qualified leads.
    
    Args:
        lead_data: Dictionary containing lead information
        
    Returns:
        dict with subject and body (plain text only)
    """
    name = lead_data.get("name", "there")
    company = lead_data.get("company", "your company")
    score = lead_data.get("score", 0)
    decision = lead_data.get("decision", "QUALIFIED")
    confidence = lead_data.get("confidence", 0)
    
    # Customize based on decision tier
    if decision == "HOT":
        subject = f"Exclusive Opportunity for {company}"
        greeting = f"Hi {name},"
        intro = f"I noticed your inquiry and wanted to reach out personally. Based on your profile, I believe we have an exceptional opportunity that aligns perfectly with {company}'s needs."
        urgency = "I'd love to schedule a call this week to discuss how we can help."
    elif decision == "QUALIFIED":
        subject = f"Great fit for {company} - Let's connect"
        greeting = f"Hello {name},"
        intro = f"Thank you for your interest! I've reviewed your information and I'm excited to discuss how we can help {company} achieve its goals."
        urgency = "I'd like to schedule a brief call within the next few days."
    elif decision == "WARM":
        subject = f"Following up on your inquiry - {company}"
        greeting = f"Hi {name},"
        intro = f"I wanted to follow up on your recent inquiry. I'd love to learn more about {company} and explore how we might be able to help."
        urgency = "Let's schedule a call when you have time."
    else:
        subject = f"Thank you for your interest"
        greeting = f"Hello {name},"
        intro = f"Thank you for reaching out to us. We'd like to learn more about {company}'s needs."
        urgency = "Feel free to reach out when you're ready to discuss further."
    
    # Plain text email body
    body = f"""{greeting}

{intro}

WHY WE THINK THIS IS A GREAT FIT:
- Match Score: {int(score * 100)}% - {decision} Priority
- Confidence Level: {int(confidence * 100)}%
- Personalized solution for {company}

I'd love to schedule a brief 15-minute call to discuss:
- Your current challenges and goals
- How our AI-powered solutions can help
- A personalized demo tailored to {company}

{urgency}

Schedule a call: https://calendly.com/your-calendar

Looking forward to connecting!

Best regards,
Your Sales Team
MatrixLead AI

---
This email was sent because you expressed interest in our services.
If you'd prefer not to receive these emails, please let us know.
"""
    
    return {
        "subject": subject,
        "body": body
    }
