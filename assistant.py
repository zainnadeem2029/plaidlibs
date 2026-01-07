"""
PlaidLibs™ OpenAI Assistant Integration Module
Handles all communication with the OpenAI Assistants API.
"""

import os
import time
from typing import Optional, Generator
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PlaidLibsAssistant:
    """Manages the OpenAI Assistant for PlaidLibs interactions."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
        self.thread_id: Optional[str] = None
        
    def create_thread(self) -> str:
        """Create a new conversation thread."""
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        return self.thread_id
    
    def get_or_create_thread(self) -> str:
        """Get existing thread or create a new one."""
        if not self.thread_id:
            return self.create_thread()
        return self.thread_id
    
    def set_thread(self, thread_id: str):
        """Set an existing thread ID."""
        self.thread_id = thread_id
    
    def send_message(self, content: str) -> str:
        """
        Send a message to the assistant and get a response.
        
        Args:
            content: The user's message content
            
        Returns:
            The assistant's response text
        """
        thread_id = self.get_or_create_thread()
        
        # Add the user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        
        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        
        # Wait for completion
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
        
        if run.status == "completed":
            # Get the latest message
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,
                order="desc",
                limit=1
            )
            
            if messages.data:
                message = messages.data[0]
                if message.content and len(message.content) > 0:
                    text_content = message.content[0]
                    if hasattr(text_content, 'text'):
                        return text_content.text.value
            
            return "I apologize, but I couldn't generate a response. Please try again."
        
        elif run.status == "failed":
            error_msg = run.last_error.message if run.last_error else "Unknown error"
            return f"I encountered an issue: {error_msg}. Let's try that again!"
        
        else:
            return f"Unexpected status: {run.status}. Please try again."
    
    def stream_message(self, content: str) -> Generator[str, None, None]:
        """
        Send a message and stream the response.
        
        Args:
            content: The user's message content
            
        Yields:
            Chunks of the assistant's response
        """
        thread_id = self.get_or_create_thread()
        
        # Add the user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        
        # Run with streaming
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        ) as stream:
            for text in stream.text_deltas:
                yield text
    
    def get_thread_messages(self, limit: int = 20) -> list:
        """
        Retrieve messages from the current thread.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries with role and content
        """
        if not self.thread_id:
            return []
        
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
            order="asc",
            limit=limit
        )
        
        result = []
        for msg in messages.data:
            content = ""
            if msg.content and len(msg.content) > 0:
                text_content = msg.content[0]
                if hasattr(text_content, 'text'):
                    content = text_content.text.value
            
            result.append({
                "role": msg.role,
                "content": content
            })
        
        return result
    
    def reset_conversation(self):
        """Reset the conversation by creating a new thread."""
        self.thread_id = None
        return self.create_thread()
    
    def generate_image(self, prompt: str, size: str = "1024x1024", style: str = "vivid", quality: str = "standard") -> dict:
        """
        Generate an image using DALL-E 3.
        
        Args:
            prompt: The image generation prompt
            size: Image size - "1024x1024", "1792x1024", or "1024x1792"
            style: "vivid" for hyper-real/dramatic, "natural" for natural look
            quality: "standard" or "hd"
            
        Returns:
            Dictionary with 'url' and 'revised_prompt' keys, or 'error' key if failed
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                style=style,
                quality=quality,
                n=1
            )
            
            if response.data and len(response.data) > 0:
                image_data = response.data[0]
                return {
                    "url": image_data.url,
                    "revised_prompt": image_data.revised_prompt
                }
            else:
                return {"error": "No image data returned"}
                
        except Exception as e:
            return {"error": str(e)}


def create_assistant(name: str, instructions: str, model: str = "gpt-4-turbo-preview") -> str:
    """
    Create a new OpenAI Assistant with the given configuration.
    
    Args:
        name: Name for the assistant
        instructions: System instructions for the assistant
        model: The model to use (default: gpt-4-turbo-preview)
        
    Returns:
        The assistant ID
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=[]  # Add tools as needed
    )
    
    return assistant.id


def update_assistant(assistant_id: str, instructions: str = None, name: str = None):
    """
    Update an existing assistant.
    
    Args:
        assistant_id: The ID of the assistant to update
        instructions: New instructions (optional)
        name: New name (optional)
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    update_params = {}
    if instructions:
        update_params["instructions"] = instructions
    if name:
        update_params["name"] = name
    
    if update_params:
        client.beta.assistants.update(
            assistant_id=assistant_id,
            **update_params
        )


def get_assistant_info(assistant_id: str) -> dict:
    """
    Get information about an assistant.
    
    Args:
        assistant_id: The ID of the assistant
        
    Returns:
        Dictionary with assistant information
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    assistant = client.beta.assistants.retrieve(assistant_id)
    
    return {
        "id": assistant.id,
        "name": assistant.name,
        "model": assistant.model,
        "instructions": assistant.instructions,
        "created_at": assistant.created_at
    }
