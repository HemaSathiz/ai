"""Day 1, step 3: a terminal chatbot with memory and streaming.

Key lesson: the model has NO memory. Every request you send must include the
whole conversation so far. That history list is the "context".

Run: python 03_chatbot.py   (type 'quit' to exit)
"""
import anthropic

client = anthropic.Anthropic()

SYSTEM = "You are a helpful mentor teaching AI engineering to a senior Android developer. Be concise."

history = []  # list of {"role": "user" | "assistant", "content": str}

print("Chatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if not user_input:
        continue

    history.append({"role": "user", "content": user_input})

    print("Claude: ", end="", flush=True)
    reply = ""

    # Streaming: print tokens as they arrive instead of waiting for the full reply
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        system=SYSTEM,
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            reply += text

    print("\n")

    # Save the reply so the next turn has the full context
    history.append({"role": "assistant", "content": reply})

# TRY THIS:
# 1. Ask "My name is Hema", then "What's my name?" and it remembers.
# 2. Comment out the history.append(assistant) line and ask again. It forgets.
#    That is exactly how context works.
# 3. Print len(history) each turn and watch the conversation grow (and cost more).
