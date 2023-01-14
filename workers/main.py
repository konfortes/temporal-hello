import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from step3.main import CICDWorkflow
from step3.simulations import (
    checkout_code,
    build_image,
    deploy_image,
    check_metrics,
    notify,
    set_deployment_marker,
    rollback_deployment,
)


async def start_workers():
    client = await Client.connect("localhost:7233")
    for _ in range(1):
        w = Worker(
            client,
            task_queue="cicd-queue",
            workflows=[CICDWorkflow],
            activities=[
                checkout_code,
                build_image,
                deploy_image,
                check_metrics,
                notify,
                set_deployment_marker,
                rollback_deployment,
            ],
        )
        print(f"starting worker {w}")
        _ = asyncio.create_task(w.run())
    await asyncio.sleep(10000000000)


if __name__ == "__main__":
    asyncio.run(start_workers())
