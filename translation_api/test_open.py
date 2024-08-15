### remove this file it was for tessssssting 


from openai import OpenAI


client = OpenAI(api_key = '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')


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a translator. Translate the following text to English."},
        {"role": "user", "content": "guten morgen"}
    ]
)

print(response)

if response and 'choices' in response:
    translated_text = response.choices[0].message['content'].strip()
    print(f"Translated text: {translated_text}")
else:
    print("Translation failed.")
