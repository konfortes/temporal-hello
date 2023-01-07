from step0.helpers import synthetic_latency, unstable


@synthetic_latency(delay=2)
async def checkout_code() -> None:
    print("Code checked out")


@synthetic_latency(delay=5)
@unstable(rate=0.6)
async def build_image(tag: str) -> None:
    print(f"Image with tag {tag} built")


@synthetic_latency(delay=10)
async def deploy_image(tag: str, env: str) -> None:
    print(f"Image with tag {tag} deployed successfully to {env}...")


@synthetic_latency(delay=1)
async def set_deployment_marker(tag: str) -> None:
    print(f"Setting deployment marker for tag {tag}...")


@synthetic_latency(delay=1)
async def notify(msg: str) -> None:
    print(f"Notifying: {msg}...")


@synthetic_latency(delay=1)
async def check_metrics() -> bool:
    return True


async def rollback_deployment(tag: str, env: str) -> None:
    print(f"Rolling back deployment of tag {tag} in {env}...")
