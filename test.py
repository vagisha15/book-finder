import openai

openai_secret_key = "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"


openai.api_key = openai_secret_key
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "You are AI Bot who will generate story ideas for inspiration for an author based on the provided prompt in 500 words!"},
    {"role": "user", "content": "A futuristic AI dominated"}

  ],
  max_tokens = 2000
)
result = completion.choices[0].message
print(result["content"])