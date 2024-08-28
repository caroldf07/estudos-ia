import os

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-4-turbo", temperature=0.5)
#
# template = PromptTemplate.from_template("""
# You are a cockney fruit and vegetable seller.
# Your role is to assist your customer with their fruit and vegetable needs.
# Respond using cockney rhyming slang.
#
# Output JSON as {{"description": "your response here"}}
#
# Tell me about the following fruit: {fruit}
# """)
#
# llm_chain = template | llm | SimpleJsonOutputParser()
# response = llm_chain.invoke({"fruit": "apple"})
#
# print(response)
# ############## Chat Models #################
# instructions = SystemMessage(content="""
# You are a surfer dude, having a conversation about the surf conditions on the beach.
# Respond using surfer slang.
# """)
#
# question = HumanMessage(content="What is the weather like?")
#
# chat_llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-4-turbo", temperature=0.5)
# response = chat_llm.invoke([
#     instructions,
#     question
# ])
#
# print(response.content)
#
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a surfer dude, having a conversation about the surf conditions on the beach. Respond using surfer slang."
#         ),
#         (
#             "human",
#             "{question}"
#         )
#     ]
# )
#
# chat_chain = prompt | chat_llm | StrOutputParser()
# response = chat_chain.invoke({"question": "What is the weather like?"})
#
# print(response)

# chat_llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-4-turbo", temperature=0.5)
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a surfer dude, having a conversation about the surf conditions on the beach. Respond using surfer slang."
#         ),
#         (
#             "system",
#             "{context}"
#         ),
#         (
#             "human",
#             "{question}"
#         )
#     ]
# )
# chat_chain = prompt | chat_llm | StrOutputParser()
# current_weather = """
#     {
#         "surf": [
#             {"beach": "Fistral", "conditions": "6ft waves and offshore winds"},
#             {"beach": "Polzeath", "conditions": "Flat and calm"},
#             {"beach": "Watergate Bay", "conditions": "3ft waves and onshore winds"}
#         ]
#     }"""
# response = chat_chain.invoke({
#     "context": current_weather,
#     "question": "What is the weather like at Fistral?"
# })
# print(response)

########### Memory on chat model ############
chat_llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-4-turbo", temperature=0.5)
memory = ChatMessageHistory()


def get_memory(session_id):
    return memory


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a surfer dude, having a conversation about the surf conditions on the beach. Respond using surfer slang."
        ),
        (
            "system",
            "{context}"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human",
            "{question}"
        )
    ]
)
chat_chain = prompt | chat_llm | StrOutputParser()
chat_with_memory = RunnableWithMessageHistory(
    runnable=chat_chain,
    get_session_history=get_memory,
    input_messages_key="question",
    history_messages_key="chat_history"
)
current_weather = """
    {
        "surf": [
            {"beach": "Fistral", "conditions": "6ft waves and offshore winds"},
            {"beach": "Polzeath", "conditions": "Flat and calm"},
            {"beach": "Watergate Bay", "conditions": "3ft waves and onshore winds"}
        ]
    }"""
response = chat_with_memory.invoke({
    "context": current_weather,
    "question": "What is the weather like at Fistral?"
},
    config={"configurable": {"session_id": "none"}}
)
print(response)
response = chat_with_memory.invoke({
    "context": current_weather,
    "question": "Where am I?"
},
    config={"configurable": {"session_id": "none"}}
)
print(response)