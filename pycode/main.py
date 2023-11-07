from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
# pip install langchain openai python-dotenv


import argparse

# parse and load the .env automatically, 
# then OpenAI(), by default, look for OPENAI_API_KEY
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()

# api_key="xxxxxxxx"
# llm = OpenAI(openai_api_key=api_key)

# this is the language model
llm = OpenAI()

code_prompt = PromptTemplate(
        template="Write a very short {language} function that will {task}",
        input_variables=["language", "task"]
        )

code_promptTest = PromptTemplate(
        template="Write a test for the following {language} code:\n {code}",
        input_variables=["language", "code"],
        )



# make the chain
code_chain = LLMChain(
        llm = llm,
        prompt=code_prompt,
        output_key="code"
)

code_chainTest = LLMChain(
        llm = llm,
        prompt=code_promptTest,
        output_key="test"
        )


chain = SequentialChain(
        chains=[code_chain, code_chainTest],
        input_variables=["task", "language"],
        output_variables=["test", "code"]
        )

result = chain({
    "language": args.language,
    "task": args.task
})


# print the generated code
print(result["code"])

# print the generated test
print("========= test ===========")
print(result["test"])


