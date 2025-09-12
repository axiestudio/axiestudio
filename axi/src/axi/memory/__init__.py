"""Memory management for AXI with dynamic loading.

This module automatically chooses between full AxieStudio implementations
(when available) and AXI stub implementations (when standalone).
"""

import importlib.util

from axi.log.logger import logger


def _has_AXIESTUDIO_memory():
    """Check if AxieStudio.memory with database support is available."""
    try:
        # Check if AxieStudio.memory and MessageTable are available
        return importlib.util.find_spec("axiestudio") is not None
    except (ImportError, ModuleNotFoundError):
        pass
    except Exception as e:  # noqa: BLE001
        logger.error(f"Error checking for AxieStudio.memory: {e}")
    return False


#### TODO: This _AXIESTUDIO_AVAILABLE implementation should be changed later ####
# Consider refactoring to lazy loading or a more robust service discovery mechanism
# that can handle runtime availability changes.
_AXIESTUDIO_AVAILABLE = _has_AXIESTUDIO_memory()

# Import the appropriate implementations
if _AXIESTUDIO_AVAILABLE:
    try:
        # Import from full AxieStudio implementation
        from AxieStudio.memory import (
            aadd_messages,
            aadd_messagetables,
            add_messages,
            adelete_messages,
            aget_messages,
            astore_message,
            aupdate_messages,
            delete_message,
            delete_messages,
            get_messages,
            store_message,
        )
    except (ImportError, ModuleNotFoundError):
        # Fall back to stubs if AxieStudio import fails
        from axi.memory.stubs import (
            aadd_messages,
            aadd_messagetables,
            add_messages,
            adelete_messages,
            aget_messages,
            astore_message,
            aupdate_messages,
            delete_message,
            delete_messages,
            get_messages,
            store_message,
        )
else:
    # Use AXI stub implementations
    from axi.memory.stubs import (
        aadd_messages,
        aadd_messagetables,
        add_messages,
        adelete_messages,
        aget_messages,
        astore_message,
        aupdate_messages,
        delete_message,
        delete_messages,
        get_messages,
        store_message,
    )

# Export the available functions and classes
__all__ = [
    "aadd_messages",
    "aadd_messagetables",
    "add_messages",
    "adelete_messages",
    "aget_messages",
    "astore_message",
    "aupdate_messages",
    "delete_message",
    "delete_messages",
    "get_messages",
    "store_message",
]
