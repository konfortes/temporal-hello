import threading
from time import sleep

from step0.simulations import (
    build_image,
    check_metrics,
    checkout_code,
    deploy_image,
    notify,
    rollback_deployment,
    set_deployment_marker,
)


def main():
    tag = "1.0.0"

    print("Checking out code...")
    checkout_code()

    max_attempts = 3
    attempt = 0
    print(f"Building image with tag {tag}...")
    while attempt < max_attempts:
        try:
            build_image(tag)
            break
        except Exception:
            attempt += 1
            print(f"Caught an exception ({attempt}), retrying...")
            sleep(2)
    else:
        raise Exception("Failed to build image")

    print(f"Deploying image with tag {tag} to staging...")
    deploy_image(tag, "staging")  # 2 minutes timeout

    print("Waiting 10 minutes for metrics to stabilize...")
    sleep(600)

    if check_metrics():
        deploy_image(tag, "production")

        t1 = threading.Thread(target=notify, args=("Deployment successful"))
        t2 = threading.Thread(target=set_deployment_marker)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    else:
        rollback_deployment(tag, "staging")
        notify("Deployment failed")


if __name__ == "__main__":
    main()
