#agent A creates an outline
#agent b creates a draft based on the outline
#agent c tests the quality of the draft
#all agent prompts are dictionaries with role = system
from system_prompts import agentC_system_prompt, agentB_system_prompt,agentA_system_prompt

#creating client that sends the prompts and receives the responses
from groq import Groq
client = Groq()
conversation_history = [
                        agentB_system_prompt
                        ]
#taking prompt from the user for the topic
prompt = input("enter your prompt :")
user_prompt = {"role":"user",
               "content":prompt}

#first agent who creates an outline for the blog no loop required here
completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        agentA_system_prompt,
        user_prompt
    ]
    )
outline = completion.choices[0].message.content
blog_outline = {"role":"user",
                "content":outline}
#adding the outline into the conversation history for the agentB
conversation_history.append(blog_outline)
#this will be where the drafts are created and tested
#let it run only 2 times max so
turns = 0
while True:
    #creating the draft
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation_history
        )
    draft = completion.choices[0].message.content
    #different drafts because the agent b will see the whole conversation history and see its own responses as
    #role : assistant but if we pass that to the draft tester than it will get confused
    draft_to_be_tested = {"role":"user",
                          "content":draft}
    draft_for_conversation_history = {"role":"assistant",
                                      "content":draft}
    conversation_history.append(draft_for_conversation_history)

    #testing the draft
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            agentC_system_prompt,
            draft_to_be_tested
        ]
    )
    test_result = completion.choices[0].message.content
    test_result_for_conversation_history = {"role":"user",
                                            "content":test_result}
    conversation_history.append(test_result_for_conversation_history)
    print(test_result)
    turns+=1

    if turns == 2 or test_result.strip().upper() == "APPROVED":
        break

print(draft)
