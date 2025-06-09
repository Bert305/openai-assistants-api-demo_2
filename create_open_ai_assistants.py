import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

assistant = client.beta.assistants.create(
    name="Math Tutor2",
    instructions="You are a math tutor capable of writing and running code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()
print(thread)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Answer specific questions: 5 * 5 + 9"
)
print(message)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

while True:
    run_result = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
    if run_result.status == "completed":
        break
    elif run_result.status == "failed":
        print("Run failed. Check the error logs.")
        break
    time.sleep(2)

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

for message in reversed(messages.data):
    content = ""
    for block in message.content:
        if hasattr(block, "text"):
            content += block.text.value
    print(f"{message.role}: {content}")
