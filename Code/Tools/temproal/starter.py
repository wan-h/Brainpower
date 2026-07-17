import asyncio
import uuid
from temporalio.client import Client
from temporalio.workflow import create_nexus_client

async def main():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        "SayHelloWorkflow",
        "Temporal",
        id=f"say-hello-workflow-{uuid.uuid4()}",
        task_queue="my-task-queue",
    )
    print("Workflow result:", result)

if __name__ == "__main__":
    asyncio.run(main())