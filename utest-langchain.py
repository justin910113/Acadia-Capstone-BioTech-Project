import langchain
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import adtiam

import cfg

# Initialize the OpenAI chat model
llm = ChatOpenAI(
    api_key=adtiam.creds['llm']['openai'],
    model_name="gpt-3.5-turbo"
)

# Example 1: Simple message
print("\nExample 1: Simple Message")
messages = [HumanMessage(content="What is the capital of France?")]
response = llm.invoke(messages)
print(response.content)

# Example 2: Structured Output
print("\nExample 2: Structured Output")
# Define the structured output model
class InvestmentInfo(BaseModel):
    amount: float = Field(description="The investment amount in millions")
    quarter: str = Field(description="The quarter of the investment")
    year: int = Field(description="The year of the investment")

# Create the output parser
parser = PydanticOutputParser(pydantic_object=InvestmentInfo)

# Create a message with structured output instructions
structured_prompt = f"""
Extract the investment information from the following text.
{parser.get_format_instructions()}

Text: "we invested $10m in expanding our facilities in Q1 2025"
"""

messages = [HumanMessage(content=structured_prompt)]

# Get the response
response = llm.invoke(messages)

# Parse the response into structured format
try:
    parsed_output = parser.parse(response.content)
    print("\nStructured Output:")
    print(f"Amount: ${parsed_output.amount}M")
    print(f"Quarter: {parsed_output.quarter}")
    print(f"Year: {parsed_output.year}")
except Exception as e:
    print(f"Error parsing response: {e}")
    print("Raw response:", response.content)

