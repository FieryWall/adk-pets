import asyncio
import flows.guidence as guidence

async def start():
    current_flow = guidence.GuidanceFlow()
    await current_flow.execute()

if __name__ == "__main__":
    asyncio.run(start())