import threading
from time import sleep
from step0.helpers import retry

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

    checkout_code()

    with retry(3, 2):
        build_image(tag)
    # with retry(2, 2):
    #     deploy_image(tag, "staging")
    deploy_image(tag, "staging")

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
