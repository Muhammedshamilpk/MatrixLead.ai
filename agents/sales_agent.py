# agents/sales_agent.py
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sales_agent")

async def generate_followup(lead_data: dict):
    """
    Simulates an LLM generating a personalized follow-up message.
    In a real scenario, this would call OpenAI/Gemini API.
    """
    await asyncio.sleep(1) # Simulate LLM latency
    
    name = lead_data.get("name", "there")
    company = lead_data.get("company", "your company")
    score = lead_data.get("score", 0)
    decision = lead_data.get("decision", "REVIEW")
    
    if decision == "CONTACT":
        # High potential lead
        subject = f"Exciting opportunities for {company}"
        body = (
            f"Hi {name},\n\n"
            f"I noticed regarding {company} that you might be looking for..."
            f"Given your strong fit (Score: {score}), I'd love to chat."
        )
        return {"subject": subject, "body": body, "channel": "email"}
    else:
        # Lower potential or unsure
        return None

async def send_communication(message_payload: dict):
    """
    Mock sending the message via Email/Chat.
    """
    await asyncio.sleep(0.5) # Simulate network call
    
    if not message_payload:
        return {"status": "skipped", "reason": "No message generated"}
        
    logger.info(f"🚀 SENDING {message_payload['channel'].upper()} 🚀")
    logger.info(f"Subject: {message_payload['subject']}")
    logger.info(f"Body: {message_payload['body']}")
    
    return {"status": "sent", "channel": message_payload['channel']}
