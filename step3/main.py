import asyncio
import random
import string
from temporalio import workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy

from step3.simulations import (
    DeployContext,
    build_image,
    check_metrics,
    checkout_code,
    deploy_image,
    notify,
    rollback_deployment,
    set_deployment_marker,
)


@workflow.defn
class CICDWorkflow:
    @workflow.run
    async def run(self, tag: str) -> None:
        workflow.logger.info("Checking out code...")
        await workflow.execute_activity(checkout_code)

        workflow.logger.info(f"Building image with tag {tag}...")
        await workflow.execute_activity(
            build_image,
            tag,
            retry_policy=RetryPolicy(maximum_attempts=3, backoff_coefficient=2),
        )

        workflow.logger.info(f"Deploying image with tag {tag} to staging...")
        await workflow.execute_activity(
            deploy_image, DeployContext(tag=tag, env="staging")
        )

        workflow.logger.info("Waiting 3 minutes before checking metrics...")
        await asyncio.sleep(180)

        are_metrics_ok = await workflow.execute_activity(check_metrics)
        if are_metrics_ok:
            workflow.logger.info(f"Deploying image with tag {tag} to production...")
            await workflow.execute_activity(
                deploy_image, DeployContext(tag=tag, env="production")
            )

            workflow.logger.info("Setting deployment marker and notifying...")

            await asyncio.gather(
                workflow.execute_activity(notify, "Deployment successful"),
                workflow.execute_activity(set_deployment_marker, tag),
            )
        else:
            await workflow.execute_activity(
                rollback_deployment, DeployContext(tag=tag, env="staging")
            )
            await workflow.execute_activity(notify, "Deployment failed")


async def main():
    client = await Client.connect("localhost:7233")

    random_build = "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(6)
    )

    result = await client.execute_workflow(
        CICDWorkflow.run,
        random_build,
        id=f"build_{random}",
        task_queue="cicd-queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
