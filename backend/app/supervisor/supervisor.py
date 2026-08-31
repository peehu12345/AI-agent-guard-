"""
AI Supervisor — orchestrates Gemini API + mock fallback.
The supervisor is ADVISORY ONLY. Policy Engine has final authority.
"""
import logging
from app.supervisor.schemas import SupervisorResponse
from app.supervisor.mock_supervisor import mock_analyze
from app.supervisor.gemini_client import gemini_analyze
from app.config import settings

logger = logging.getLogger(__name__)


async def analyze(context: dict, use_llm: bool = True) -> tuple[SupervisorResponse, bool]:
    """
    Analyze a transaction context and return a recommendation.
    
    Returns:
        (SupervisorResponse, used_llm: bool)
        used_llm=True means real Gemini API was used
        used_llm=False means mock supervisor was used
    """
    # Try real LLM if API key is configured and use_llm is True
    if use_llm and settings.gemini_api_key:
        llm_result = await gemini_analyze(context)
        if llm_result is not None:
            logger.info(f"Gemini AI Supervisor responded for {context.get('customer_id')}")
            return llm_result, True

    # Fallback to mock supervisor
    mock_result = mock_analyze(context)
    logger.debug(f"Mock supervisor used for {context.get('customer_id')}")
    return mock_result, False
