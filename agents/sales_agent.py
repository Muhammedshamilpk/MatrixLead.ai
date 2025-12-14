# agents/sales_agent.py
import asyncio
import logging
from email_service import EmailService, generate_qualified_lead_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sales_agent")

# Initialize email service
email_service = EmailService()


async def generate_followup(lead_data: dict):
    """
    Generate a personalized follow-up message for qualified leads.
    Uses plain text email templates based on qualification tier.
    """
    await asyncio.sleep(0.5)  # Simulate processing time
    
    decision = lead_data.get("decision", "REVIEW")
    email = lead_data.get("email")
    
    # Only generate emails for qualified leads
    if decision in ["HOT", "QUALIFIED", "WARM"]:
        if not email:
            logger.warning(f"Lead {lead_data.get('lead_id')} has no email address")
            return None
        
        # Generate personalized email content
        email_content = generate_qualified_lead_email(lead_data)
        
        return {
            "to_email": email,
            "subject": email_content["subject"],
            "body": email_content["body"],
            "channel": "email",
            "decision": decision
        }
    else:
        # Don't send emails for NURTURE, REVIEW, or NOT_QUALIFIED
        logger.info(f"Lead {lead_data.get('lead_id')} decision '{decision}' - no immediate email sent")
        return None


async def send_communication(message_payload: dict):
    """
    Send the message via Email using SMTP (plain text only).
    """
    if not message_payload:
        return {"status": "skipped", "reason": "No message generated"}
    
    try:
        to_email = message_payload.get("to_email")
        subject = message_payload.get("subject")
        body = message_payload.get("body")
        decision = message_payload.get("decision", "QUALIFIED")
        
        if not to_email:
            logger.error("❌ Aborting email send: 'to_email' is missing!")
            return {"status": "skipped", "reason": "No recipient email provided"}

        logger.info(f"🚀 ATTEMPTING EMAIL SEND 🚀")
        logger.info(f"   FROM: {email_service.from_email}")
        logger.info(f"   TO:   {to_email}")
        logger.info(f"   SUBJ: {subject}")
        
        # Send email using the email service (plain text only)
        result = email_service.send_email(
            to_email=to_email,
            subject=subject,
            body_text=body
        )
        
        if result["status"] == "sent":
            logger.info(f"✅ Email successfully sent to {to_email}")
            return {
                "status": "sent",
                "channel": "email",
                "to": to_email,
                "subject": subject,
                "decision": decision
            }
        else:
            logger.error(f"❌ Failed to send email: {result.get('message')}")
            return {
                "status": "failed",
                "channel": "email",
                "error": result.get("message"),
                "to": to_email
            }
            
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")
        return {
            "status": "error",
            "channel": "email",
            "error": str(e)
        }

