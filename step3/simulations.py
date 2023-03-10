from dataclasses import dataclass
from step3.helpers import synthetic_latency, unstable

from temporalio import activity


@dataclass
class DeployContext:
    tag: str
    env: str


@activity.defn(name="checkout_code")
@synthetic_latency(delay=2)
async def checkout_code() -> None:
    print("Code checked out")


@activity.defn(name="build_image")
@synthetic_latency(delay=5)
@unstable(rate=0.6)
async def build_image(tag: str) -> None:
    print(f"Image with tag {tag} built")


@activity.defn(name="deploy_image")
@synthetic_latency(delay=10)
async def deploy_image(context: DeployContext) -> None:
    print(f"Image with tag {context.tag} deployed successfully to {context.env}...")


@activity.defn(name="set_deployment_marker")
@synthetic_latency(delay=1)
async def set_deployment_marker(tag: str) -> None:
    print(f"Setting deployment marker for tag {tag}...")


@activity.defn(name="notify")
@synthetic_latency(delay=1)
async def notify(msg: str) -> None:
    print(f"Notifying: {msg}...")


@activity.defn(name="check_metrics")
@synthetic_latency(delay=1)
async def check_metrics() -> bool:
    return True


@activity.defn(name="rollback_deployment")
@synthetic_latency(delay=1)
async def rollback_deployment(context: DeployContext) -> None:
    print(f"Rolling back deployment of tag {context.tag} in {context.env}...")
