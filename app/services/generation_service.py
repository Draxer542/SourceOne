from typing import List, AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, trim_messages
from app.core.config import settings
from app.core.logging import logger
from app.models import Message

class GenerationService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="openai/gpt-oss-20b",
            openai_api_key=settings.NVIDIA_API_KEY,
            temperature=0.5,
            streaming=True,
            openai_api_base="https://integrate.api.nvidia.com/v1"
        )
        
        # 1. Answer Generation Prompt (Optimized for Standalone Query + Context)
        self.answer_prompt = ChatPromptTemplate.from_template(
            """
            Role: You are an expert AI assistant designed to provide accurate answers based on the provided context.
            
            Instructions:
            1. Use ONLY the information provided in the "Context" section below to answer the user's question.
            2. If the answer cannot be found in the context, state clearly that you don't have enough information. Do not fabricate answers.
            3. Format your response using clear and professional Markdown:
               - Use headers (#, ##, ###) to structure the answer.
               - Use bullet points or numbered lists for steps or lists.
               - Use bolding (**text**) for key concepts.
               - Use code blocks (```language ... ```) for code snippets.
            4. Be concise but thorough.
              
            Context:
            {context}
            
            Question: 
            {question}
            """
        )
        self.answer_chain = self.answer_prompt | self.llm | StrOutputParser()

        # 2. Contextualization Prompt (History-Aware)
        self.context_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        self.context_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.context_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        self.context_chain = self.context_prompt | self.llm | StrOutputParser()

    def format_history(self, db_messages: List[Message]) -> List[BaseMessage]:
        """Convert DB messages to LangChain format."""
        history = []
        for msg in db_messages:
            if msg.role == "user":
                history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                history.append(AIMessage(content=msg.content))
        return history

    async def contextualize_query(self, query: str, history: List[BaseMessage]) -> str:
        """
        Rewrites the query to be standalone based on history.
        Uses trim_messages to ensure token efficiency (last 4 messages).
        """
        if not history:
            logger.info("No history provided. Using original query.")
            return query
            
        logger.info(f"Contextualizing query: '{query}' with {len(history)} history messages.")
        for i, msg in enumerate(history):
            logger.info(f"History[{i}] ({msg.type}): {msg.content}")
        
        # Trim history to manage tokens explicitly
        trimmed_history = trim_messages(
            history,
            max_tokens=500, # Approximate token limit for history context
            strategy="last",
            token_counter=len, # Fallback simple counter if model not passed, or use llm property
            include_system=False,
            start_on="human"
        )
        logger.info(f"Trimmed History size: {len(trimmed_history)}")
        
        try:
            standalone_query = await self.context_chain.ainvoke({
                "chat_history": trimmed_history,
                "question": query
            })
            logger.info(f"Original Query: '{query}' -> Standalone Query: '{standalone_query}'")
            return standalone_query
        except Exception as e:
            logger.error(f"Contextualization failed: {e}")
            return query

    async def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        """
        Generates an answer using the LLM based on the query and retrieved context.
        """
        logger.info("Generating answer...")
        
        # Format context
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        try:
            response = await self.answer_chain.ainvoke({
                "context": context_text,
                "question": query
            })
            logger.info("Answer generated successfully.")
            return response
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Sorry, I encountered an error while generating the answer."

    async def generate_answer_stream(self, query: str, context_docs: List[Document]) -> AsyncGenerator[str, None]:
        """
        Streams the answer using the LLM based on the query and retrieved context.
        """
        logger.info("Streaming answer generation...")
        
        # Log retrieved docs for debugging
        for i, doc in enumerate(context_docs):
            logger.info(f"Context Doc [{i}]: {doc.page_content[:200]}...") # Log first 200 chars

        # Format context
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        try:
            # Build the prompt
            prompt_text = self.answer_prompt.format(context=context_text, question=query)
            logger.info(f"Final Generation Prompt: {prompt_text[:500]}...") # Log prompt start
            
            # Stream using the LLM directly
            async for chunk in self.llm.astream(prompt_text):
                if chunk.content:
                    yield chunk.content
            
            logger.info("Stream generation completed successfully.")
        except Exception as e:
            logger.error(f"Error in stream generation: {e}")
            yield f"Error: {str(e)}"

generation_service = GenerationService()
