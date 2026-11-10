"""Day 1, step 2: get structured JSON back from the model.

This is the basis of most real AI features: turn messy text into data your
code can use (think: receipt text -> expense record in your Android app).

Run: python 02_structured_output.py
"""
import json
import anthropic

client = anthropic.Anthropic()

receipt_text = """
WOOLWORTHS METRO COLLINS ST
12/10/2026  14:32
Milk 2L            4.20
Sourdough          6.50
Bananas 1.2kg      4.80
TOTAL             15.50
Paid by VISA
"""

system_prompt = """You extract data from receipts.
Respond with ONLY valid JSON, no explanation and no markdown fences, in this shape:
{"merchant": string, "date": "YYYY-MM-DD", "total": number, "category": string,
 "items": [{"name": string, "price": number}]}"""

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2000,
    system=system_prompt,
    messages=[{"role": "user", "content": receipt_text}],
)

raw = "".join(block.text for block in response.content if block.type == "text")

# Never trust model output blindly: always parse defensively
try:
    data = json.loads(raw)
    print(json.dumps(data, indent=2))
    print(f"\nTotal as a number: {data['total']}")
except json.JSONDecodeError:
    print("Model did not return valid JSON:")
    print(raw)

# TRY THIS: paste a different receipt, or remove the "ONLY valid JSON"
# instruction and see what breaks. That failure is why validation matters.
