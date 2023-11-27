from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import openai_api_key

import os

os.environ['OPENAI_API_KEY'] = openai_api_key

llm = OpenAI(temperature=0.7)


def generate_restaurant_name_and_items(cuisine):
    # chain1 : restaurant Name
    prompt_names = PromptTemplate(
        input_variables=['cuisine'],
        template="i want to open a restaurant for {cuisine} food. Suggest a fancy restaurant name."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_names, output_key="restaurant_name")

    # chain 2: Food items

    prompt_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as comma seperated list."
    )

    food_item_chain = LLMChain(llm=llm, prompt=prompt_items, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_item_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']

    )

    response = chain({'cuisine': 'German'})

    return response


if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"))
