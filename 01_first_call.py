"""Day 1, step 1: your first LLM API call.

Run: python 01_first_call.py
"""
import anthropic

# Reads ANTHROPIC_API_KEY from your environment automatically
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2000,
    # The system prompt sets the model's role and behaviour
    system="You are a patient mentor helping a senior Android engineer learn AI engineering.",
    messages=[
        {"role": "user", "content": "Explain what a context window is, using an Android analogy."}
    ],
)

# The reply is a list of content blocks; the first one is the text
text = "".join(block.text for block in response.content if block.type == "text")
print(text)

# Tokens are what you are billed for, so get used to checking them
print(f"\nTokens used -> input: {response.usage.input_tokens}, output: {response.usage.output_tokens}")

# TRY THIS: change the system prompt (e.g. "Reply in exactly two sentences")
# and see how the output changes.
