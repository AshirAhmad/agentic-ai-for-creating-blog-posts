"""Groq AI chat client with conversation history."""

from groq import Groq

# Conversation history including system instructions for context
conversation_history = [
    {
        "role": "system",
        "content": "you are a useful and helpful assistant, keep your response short and to the point"
    }
]

client = Groq()
prompt = input("please enter your prompt :")

while prompt != "end":
    conversation_history.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation_history
    )

    response = completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response})
    print(response)
    prompt = input("enter your prompt :")

print("the loop has ended thanks for using our ai")