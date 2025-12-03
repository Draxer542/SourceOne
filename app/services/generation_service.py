from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from app.core.config import settings
from app.core.logging import logger

class GenerationService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful assistant. Answer the user's question based ONLY on the following context. 
            If the answer is not in the context, say "I don't know based on the provided documents."
            
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

generation_service = GenerationService()
