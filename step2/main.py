import asyncio

from step2.simulations import (
    build_image,
    check_metrics,
    checkout_code,
    deploy_image,
    notify,
    rollback_deployment,
    set_deployment_marker,
)


async def main():
    tag = "1.0.0"

    print("Checking out code...")
    await checkout_code()

    max_attempts = 3
    attempt = 0
    print(f"Building image with tag {tag}...")
    while attempt < max_attempts:
        try:
            await build_image(tag)
            break
        except Exception:
            attempt += 1
            print(f"Caught an exception ({attempt}), retrying...")
            await asyncio.sleep(2)
    else:
        raise Exception("Failed to build image")

    print(f"Deploying image with tag {tag} to staging...")
    await deploy_image(tag, "staging")

    print("Waiting 10 minutes before checking metrics...")
    await asyncio.sleep(600)

    if await check_metrics():
        print(f"Deploying image with tag {tag} to production...")
        await deploy_image(tag, "production")

        print("Setting deployment marker and notifying...")
        await asyncio.gather(
            notify("Deployment successful"), set_deployment_marker(tag)
        )
    else:
        await rollback_deployment(tag, "staging")
        await notify("Deployment failed")


if __name__ == "__main__":
    asyncio.run(main())
