# <-- 1. Import the Plugin -->
from google.adk.plugins.logging_plugin import (LoggingPlugin,)
from google.adk.runners import InMemoryRunner
from enum import Enum

class Role(Enum):
    USER = "User"
    AGENT = "Agent"

def display(role: Role, message: str) -> str:
    print(f"{role.value}: {message}\n")
    return message

# <-- 2. Add the Plugin. Handles standard Observability logging across ALL agents -->
def _create_logging_plugin():
    """Create a LoggingPlugin instance with best-effort compatibility across ADK versions."""
    fmt = "{timestamp} - {agent_name} - {role}: {message}"
    # Try the most likely constructor signature first, then fall back to alternatives.
    try:
        return LoggingPlugin(log_level="INFO", log_format=fmt, log_destination="console")
    except TypeError:
        pass

    try:
        return LoggingPlugin(level="INFO", format=fmt, destination="console")
    except TypeError:
        pass

    try:
        # Last resort: instantiate with no args and attempt to set attributes if available.
        plugin = LoggingPlugin()
        for attr, value in (('log_level', 'INFO'), ('log_format', fmt), ('log_destination', 'console')):
            if hasattr(plugin, attr):
                try:
                    setattr(plugin, attr, value)
                except Exception:
                    pass
        return plugin
    except Exception:
        return None


_plugin = _create_logging_plugin()
try:
    if _plugin is not None:
        try:
            runner = InMemoryRunner(plugins=[_plugin])
        except TypeError:
            try:
                runner = InMemoryRunner(plugin=_plugin)
            except TypeError:
                runner = InMemoryRunner()
    else:
        runner = InMemoryRunner()
except Exception:
    # If creating an InMemoryRunner fails for any reason, set runner to None so importing this module
    # doesn't raise. The application can create the runner at runtime as needed.
    runner = None
