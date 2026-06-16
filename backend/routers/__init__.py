"""
Routers package
"""

from .xrd import router as xrd_router
from .auth import router as auth_router, visitor_router
from .news import router as news_router
from .molecule import router as molecule_router
from .molecule_open import router as molecule_open_router
from .materials import router as materials_router
from .literature import router as literature_router
from .admin import router as admin_router
from .upload import router as upload_router
from agent import agent_router

__all__ = ["xrd_router", "auth_router", "visitor_router", "agent_router", "news_router", "molecule_router", "molecule_open_router", "materials_router", "literature_router", "admin_router", "upload_router"]
