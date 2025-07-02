"""
Example of using Azure OpenAI with magentic-ui
"""
import asyncio
import os
from typing import Optional
from magentic_ui.magentic_ui_config import MagenticUIConfig, ModelClientConfigs
from magentic_ui.teams import GroupChat
from magentic_ui.agents import WebSurfer, CoderAgent, FileSurfer
from magentic_ui.agents.users import DummyUserProxy
from magentic_ui.types import RunPaths
from magentic_ui.utils import get_internal_urls
from magentic_ui.tools.playwright.browser import get_browser_resource_config
from magentic_ui.teams.orchestrator.orchestrator_config import OrchestratorConfig
from magentic_ui.agents.web_surfer import WebSurferConfig

async def create_azure_team() -> GroupChat:
    """Create a team using Azure OpenAI"""
    
    # Set environment variables
    os.environ["AZURE_OPENAI_API_KEY"] = "9FNrC8BdOJqArMJRfoC3lk6tpjkQZ3dLDfccEGR4wLnvJTf1mIO6JQQJ99BCACHYHv6XJ3w3AAAAACOGyxtr"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://dctassistresou5125686331.cognitiveservices.azure.com"
    os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
    
    # Azure OpenAI configuration
    azure_client_config = {
        "provider": "AzureOpenAIChatCompletionClient",
        "config": {
            "model": "gpt-4o",
            "azure_endpoint": "https://dctassistresou5125686331.cognitiveservices.azure.com",
            "api_version": "2024-02-15-preview",
            "azure_deployment": "gpt-4o"
        },
        "max_retries": 5
    }
    
    # Create model client configs with Azure OpenAI
    model_client_configs = ModelClientConfigs(
        orchestrator=azure_client_config,
        web_surfer=azure_client_config,
        coder=azure_client_config,
        file_surfer=azure_client_config,
        action_guard=azure_client_config
    )
    
    # Create magentic-ui config
    magentic_config = MagenticUIConfig(
        model_client_configs=model_client_configs,
        cooperative_planning=True,
        autonomous_execution=False,
        max_turns=10,
        approval_policy="auto-conservative"
    )
    
    # Setup paths (adjust as needed)
    paths = RunPaths(
        internal_run_dir="/tmp/magentic_ui_run",
        external_run_dir="/tmp/magentic_ui_run",
        internal_root_dir="/tmp/magentic_ui",
        external_root_dir="/tmp/magentic_ui"
    )
    
    # Create browser config
    browser_resource_config, _, _ = get_browser_resource_config(
        paths.external_run_dir,
        -1,  # novnc_port
        -1,  # playwright_port
        False,  # inside_docker
        headless=True,
        local=True
    )
    
    # Create websurfer config
    websurfer_config = WebSurferConfig(
        name="web_surfer",
        model_client=azure_client_config,
        browser=browser_resource_config,
        single_tab_mode=False,
        max_actions_per_step=5,
        downloads_folder=str(paths.internal_run_dir),
        debug_dir=str(paths.internal_run_dir),
        animate_actions=True,
        start_page=None,
        use_action_guard=True,
        to_save_screenshots=False,
    )
    
    # Create orchestrator config
    orchestrator_config = OrchestratorConfig(
        cooperative_planning=True,
        autonomous_execution=False,
        model_context_token_limit=110000,
        do_bing_search=False,
        retrieve_relevant_plans="never",
        allow_follow_up_input=True
    )
    
    # Create agents
    user_proxy = DummyUserProxy(name="user_proxy")
    
    web_surfer = WebSurfer.from_config(websurfer_config)
    
    coder_agent = CoderAgent(
        name="coder_agent",
        model_client=azure_client_config,
        work_dir=paths.internal_run_dir,
        bind_dir=paths.external_run_dir,
        model_context_token_limit=110000
    )
    
    file_surfer = FileSurfer(
        name="file_surfer",
        model_client=azure_client_config,
        work_dir=paths.internal_run_dir,
        bind_dir=paths.external_run_dir,
        model_context_token_limit=110000
    )
    
    # Create team
    team = GroupChat(
        participants=[web_surfer, user_proxy, coder_agent, file_surfer],
        orchestrator_config=orchestrator_config,
        model_client=azure_client_config
    )
    
    await team.lazy_init()
    print("✅ Azure OpenAI team created successfully!")
    
    return team

async def main():
    """Main function to test Azure OpenAI integration"""
    try:
        team = await create_azure_team()
        print("🎉 Ready to use magentic-ui with Azure OpenAI!")
        
        # You can now use the team for tasks
        # Example: await team.run("Your task here")
        
    except Exception as e:
        print(f"❌ Error creating Azure team: {e}")
        print("Please check your Azure OpenAI configuration")

if __name__ == "__main__":
    asyncio.run(main())
