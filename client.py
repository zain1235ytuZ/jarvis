from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)
