from typing import List, AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logging import logger

class GenerationService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="openai/gpt-oss-20b",
            openai_api_key=settings.NVIDIA_API_KEY,
            temperature=0.5,
            streaming=True,
            openai_api_base="https://integrate.api.nvidia.com/v1"
        )
        self.prompt = ChatPromptTemplate.from_template(
            """
            Role: You are a precise and helpful assistant.
            
            Instructions: 
            1. Answer the user's question strictly based on the provided context.
            2. Do not include any information specifically not present in the context.
            3. Preserve the original formatting of the context (e.g., markdown tables, lists, code blocks) in your answer.
            4. Do not add introductory or concluding chatter (e.g., "Based on the context...", "Here is the answer..."). Just provide the answer.
            5. If the answer is not in the context, state that you don't know based on the provided documents.

            Context:
            {context}
            
            Question: 
            {question}
            """
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        """
        Generates an answer using the LLM based on the query and retrieved context.
        """
        logger.info("Generating answer...")
        
        # Format context
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        try:
            response = await self.chain.ainvoke({
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
        Yields text chunks as they are generated, with proper space handling.
        """
        logger.info("Streaming answer generation...")
        
        # Format context
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        try:
            # Build the prompt
            prompt_text = self.prompt.format(context=context_text, question=query)
            
            # Stream using the LLM directly
            async for chunk in self.llm.astream(prompt_text):
                if chunk.content:
                    yield chunk.content
            
            logger.info("Stream generation completed successfully.")
        except Exception as e:
            logger.error(f"Error in stream generation: {e}")
            yield f"Error: {str(e)}"

generation_service = GenerationService()
