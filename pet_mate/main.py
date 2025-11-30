import asyncio
import os
import sys
import signal
from settings import parse_args
from logger import setup_logger
from state import State
from flows import GuidanceFlow


class ShutdownHandler:
    def __init__(self):
        self.event = asyncio.Event()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        self.event.set()


async def start():
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    parse_args()
    setup_logger()
    
    shutdown = ShutdownHandler()
    state = State()
    await state.reset()
    
    guidance_flow = GuidanceFlow(state, shutdown.event)
    await guidance_flow.setup()
    
    try:
        await guidance_flow.run()
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        pass
    finally:
        shutdown.event.set()
        try:
            await guidance_flow.cleanup()
        except Exception:
            pass
        
        try:
            current_task = asyncio.current_task()
            pending = [task for task in asyncio.all_tasks() if task != current_task]
            for task in pending:
                task.cancel()
            
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
        except Exception:
            pass
        
        await asyncio.sleep(0.2)


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("\n[App] Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"[App] Error: {e}")
        sys.exit(1)