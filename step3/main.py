import asyncio
from datetime import timedelta
import sys
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
        await workflow.execute_activity(
            checkout_code,
            start_to_close_timeout=timedelta(minutes=3),
        )

        workflow.logger.info(f"Building image with tag {tag}...")
        await workflow.execute_activity(
            build_image,
            tag,
            retry_policy=RetryPolicy(maximum_attempts=3, backoff_coefficient=2),
            start_to_close_timeout=timedelta(minutes=1),
        )

        workflow.logger.info(f"Deploying image with tag {tag} to staging...")
        await workflow.execute_activity(
            deploy_image,
            DeployContext(tag=tag, env="staging"),
            start_to_close_timeout=timedelta(minutes=2),
        )

        workflow.logger.info("Waiting 3 minutes before checking metrics...")
        await asyncio.sleep(180)

        are_metrics_ok = await workflow.execute_activity(
            check_metrics,
            start_to_close_timeout=timedelta(minutes=1),
        )
        if are_metrics_ok:
            workflow.logger.info(f"Deploying image with tag {tag} to production...")
            await workflow.execute_activity(
                deploy_image,
                DeployContext(tag=tag, env="production"),
                start_to_close_timeout=timedelta(minutes=1),
            )

            workflow.logger.info("Setting deployment marker and notifying...")

            await asyncio.gather(
                workflow.execute_activity(
                    notify,
                    "Deployment successful",
                    start_to_close_timeout=timedelta(minutes=1),
                ),
                workflow.execute_activity(
                    set_deployment_marker,
                    tag,
                    start_to_close_timeout=timedelta(minutes=1),
                ),
            )
        else:
            await workflow.execute_activity(
                rollback_deployment,
                DeployContext(tag=tag, env="staging"),
                start_to_close_timeout=timedelta(minutes=1),
            )
            await workflow.execute_activity(
                notify,
                "Deployment failed",
                start_to_close_timeout=timedelta(minutes=1),
            )


async def main():
    client = await Client.connect("localhost:7233")

    tag = "1.0.0" if not len(sys.argv) > 1 else sys.argv[1]
    await client.execute_workflow(
        CICDWorkflow.run,
        tag,
        id=f"build_{tag}",
        task_queue="cicd-queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
