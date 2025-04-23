import os
from groq import Groq
import base64
from IPython.display import Image
import requests
import json
from dotenv import find_dotenv , load_dotenv
##

load_dotenv(find_dotenv())

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# model = 'llama-3.2-90b-vision-preview'
model = 'llama-3.2-11b-vision-preview'
ninja_api_key = os.environ.get('NINJA_API_KEY')
image_path = r"C:\Users\Orion\german.jpeg"

Image(image_path)

def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)

# user_prompt = input("Enter a prompt: ")
user_prompt = "What is the breed of this animal in this image?, answer Only by giving it's name"
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            "content":[{
                "type":"image_url",
                "image_url":{
                    "url":f"data:image/jpeg;base64,{base64_image}"
                },

            },
                {
                    "type":"text",
                    "text":user_prompt
                }
            ],
        }
    ],
    model=model
)
print(chat_completion.choices[0].message.content)

## funcyion to vget dog breed
def get_dog_facts(breed_name):
    api_url = "https://api.api-ninjas.com/v1/dogs?name={}".format(breed_name)
    response = requests.get(api_url , headers={'X-Api-Key':ninja_api_key})
    ## check request
    if response.status_code == requests.codes.ok:
        top_match = response.json()[0]
        return top_match
    else: return "Error",response.status_code , response.text

# get_dog_breed(dog)


#### Now make a tool
tools =[
    {
        "type":"function",
        "function":{
            "name":"get_dog_facts",
            "description":"Give facts about your dog breed",
            "parameters":{
                "type":"object",
                "properties":{
                    "breed_name":{"type":"string" , "description":"The name of dog breed" }
                },
                "required":"[breed_name]"
            },
        },
    }
]

### now function to call that tools:
def llama_vision_tool_call(client, model, base64_image, available_functions):
    chat_completion = client.chat.completions.create(
        # the user message containg image
    messages=[
        {
            "role":"user",
            "content":[
                {
                    "type":"image_url",
                    "image_url":{"url":f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
        model=model,
        tools=tools,
        tool_choice = "auto"
    )

    response_message =chat_completion.choices[0].message
    tool_calls = response_message.tool_calls
    for tool_call in tool_calls:
        # Get the function name from the tool call
        function_name = tool_call.function.name

        # Get the function to call from the available functions dictionary
        function_to_call = available_functions[function_name]

        # Parse the function arguments from the tool call
        function_args = json.loads(tool_call.function.arguments)

        # Call the function with the breed name
        function_response = function_to_call(
            breed_name=function_args.get("breed_name")
        )
        return function_response

# Define available functions
available_functions = {
    "get_dog_facts": get_dog_facts,  # Example function to get dog facts

}

dog_breed_json = llama_vision_tool_call(client, model, base64_image, available_functions)
# print(dog_breed_json)
dog_desc ="""
   
    1. Shedding:
       - Description: How much hair the breed sheds.
       - Possible values: 1 to 5 (where 1 indicates no shedding and 5 indicates maximum shedding).
    
    2. Barking:
       - Description: How vocal the breed is.
       - Possible values: 1 to 5 (where 1 indicates minimal barking and 5 indicates maximum barking).
    
    3. Energy:
       - Description: How much energy the breed has.
       - Possible values: 1 to 5 (where 1 indicates low energy and 5 indicates high energy).
    
    4. Protectiveness:
       - Description: How likely the breed is to alert strangers.
       - Possible values: 1 to 5 (where 1 indicates minimal alerting and 5 indicates maximum alerting).
    
    5. Trainability:
       - Description: How easy it is to train the breed.
       - Possible values: 1 to 5 (where 1 indicates the breed is very difficult to train and 5 indicates the breed is very easy to train).
    
    6. Name:
       - Description: The name of the breed.
    
    7. Min Height:
       - Description: Minimum height in inches.
    
    8. Max Height:
       - Description: Maximum height in inches.
    
    9. Min Weight:
       - Description: Minimum weight in pounds.
    
    10. Max Weight:
       - Description: Maximum weight in pounds.
    
    11. Min Life Expectancy:
       - Description: Minimum life expectancy in years.
    
    12. Max Life Expectancy:
       - Description: Maximum life expectancy in years.
    
  
"""

def assess_dog_breed(client, model,dog_breed_json):
    user_message=f"""
         Write an assessment of this breed according to given json if its dog or cat given the JSON info provided; below is a description for dog and cat breed of the  fields in the JSON:
    
    {dog_breed_json}
    Description:   
    {dog_desc}

       """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ],
        # model="deepseek-r1-distill-llama-70b",
        # model="llama-3.3-70b-specdec",
        model="llama3-70b-8192", ## this and above give sligtly more information about dog health issue
        # model="mixtral-8x7b-32768",
        # temperature=1,

    )

    return chat_completion.choices[0].message.content
dog_breed_assessment = assess_dog_breed(client, model, dog_breed_json)
print(dog_breed_assessment)