from step0.helpers import synthetic_latency, unstable


@synthetic_latency(delay=2)
def checkout_code() -> None:
    print("Checking out code...")


@synthetic_latency(delay=5)
@unstable(rate=0.6)
def build_image(tag: str) -> None:
    print(f"Building image with tag {tag}...")


@synthetic_latency(delay=10)
# @unstable(rate=0.1)
def deploy_image(tag: str, env: str) -> None:
    print(f"Deploying image with tag {tag} to {env}...")


@synthetic_latency(delay=1)
def set_deployment_marker(tag: str) -> None:
    print(f"Setting deployment marker for tag {tag}...")


@synthetic_latency(delay=1)
def notify(msg: str) -> None:
    print("Notifying: {msg}...")


@synthetic_latency(delay=1)
def check_metrics() -> bool:
    return True


def rollback_deployment(tag: str, env: str) -> None:
    print(f"Rolling back deployment of tag {tag} in {env}...")
