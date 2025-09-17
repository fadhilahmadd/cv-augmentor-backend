from langchain_google_genai import ChatGoogleGenerativeAI

# predictable tasks like parsing
strict_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# creative tasks like report writing
creative_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)