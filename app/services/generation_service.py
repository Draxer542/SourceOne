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
            previous_chunk = ""
            async for chunk in self.llm.astream(prompt_text):
                if chunk.content:
                    current_chunk = chunk.content
                    yield current_chunk
                    previous_chunk = current_chunk
            
            logger.info("Stream generation completed successfully.")
        except Exception as e:
            logger.error(f"Error in stream generation: {e}")
            yield f"Error: {str(e)}"

generation_service = GenerationService()
