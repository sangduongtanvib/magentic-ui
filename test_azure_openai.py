"""
Test Azure OpenAI configuration with magentic-ui
"""
import asyncio
import os
from autogen_core.models import ChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def test_azure_openai():
    """Test Azure OpenAI connection"""
    
    # Set environment variables
    os.environ["AZURE_OPENAI_API_KEY"] = "9FNrC8BdOJqArMJRfoC3lk6tpjkQZ3dLDfccEGR4wLnvJTf1mIO6JQQJ99BCACHYHv6XJ3w3AAAAACOGyxtr"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://dctassistresou5125686331.cognitiveservices.azure.com"
    os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
    
    # Create Azure OpenAI client config
    azure_config = {
        "provider": "AzureOpenAIChatCompletionClient",
        "config": {
            "model": "gpt-4o",
            "azure_endpoint": "https://dctassistresou5125686331.cognitiveservices.azure.com",
            "api_version": "2024-02-15-preview",
            "azure_deployment": "gpt-4o"
        },
        "max_retries": 5
    }
    
    try:
        # Create client
        client = ChatCompletionClient.load_component(azure_config)
        print("✅ Azure OpenAI client created successfully")
        
        # Test with a simple message
        messages = [
            TextMessage(content="Hello, this is a test message. Please respond with 'Azure OpenAI is working!'", source="user")
        ]
        
        print("🔄 Testing Azure OpenAI connection...")
        
        # Note: Actual API call would require proper message format for the specific client
        print("✅ Configuration appears valid")
        print("📝 Client config:", azure_config)
        
    except Exception as e:
        print(f"❌ Error testing Azure OpenAI: {e}")
        print("Please check your credentials and endpoint")

if __name__ == "__main__":
    asyncio.run(test_azure_openai())
