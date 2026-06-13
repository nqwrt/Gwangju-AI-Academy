from openai import OpenAI

api_key = 'sk-'	

client = OpenAI(api_key=api_key)

from openai import OpenAI

client = OpenAI(
    api_key=api_key
)

response = client.responses.create(
    model="gpt-4o-mini",
    input="2022년 월드컵 우승팀은 어디야?"
)

print(response.output_text)


#예전스타일
# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   temperature=0.1,  
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "2022년 월드컵 우승팀은 어디야?"},
#   ]		
# )

# print(response)

# print('----')	
# print(response.choices[0].message.content) 