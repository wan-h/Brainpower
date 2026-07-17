from temporalio import activity

@activity.defn
async def greet(name: str) -> str:
    return f"Hello {name}"