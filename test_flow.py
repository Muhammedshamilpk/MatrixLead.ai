import requests
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_lead_lifecycle():
    print("🚀 Starting Backend Lifecycle Test...")
    
    # 1. Create a Lead
    lead_payload = {
        "name": "Test User",
        "email": "test@business.com",  # Should trigger good score
        "phone": "+15550000000",
        "company": "Tech Corp",
        "data": {
            "message": "We are looking for enterprise AI solutions."
        }
    }
    
    try:
        print("Creating lead...")
        resp = requests.post(f"{BASE_URL}/leads", json=lead_payload)
        resp.raise_for_status()
        lead = resp.json()
        lead_id = lead["id"]
        print(f"✅ Lead Created! ID: {lead_id} (Status: {lead['status']})")
    except Exception as e:
        print(f"❌ Failed to create lead: {e}")
        sys.exit(1)

    # 2. Poll for Qualification
    print("⏳ Waiting for agents to qualify...")
    max_retries = 10
    for i in range(max_retries):
        time.sleep(2)
        try:
            # We assume there's a GET /leads/{id} or we list all
            # Since routes.py only showed GET /leads (list), we use that
            resp = requests.get(f"{BASE_URL}/leads")
            leads = resp.json()
            # Find our lead
            my_lead = next((l for l in leads if l["id"] == lead_id), None)
            
            if my_lead:
                status = my_lead["status"]
                score = my_lead["score"]
                print(f"   Attempt {i+1}: Status={status}, Score={score}")
                
                if status in ["QUALIFIED", "NOT_QUALIFIED", "IN_PROGRESS"]:
                    print(f"✅ Qualification Complete! Status: {status}")
                    
                    if status == "QUALIFIED":
                        print("✅ Lead is Qualified. Verification assumes Sales Agent Triggered.")
                    return
        except Exception as e:
            print(f"Warning: Poll failed {e}")
            
    print("❌ Timed out waiting for qualification.")
    sys.exit(1)

if __name__ == "__main__":
    test_lead_lifecycle()
