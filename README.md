# Temporal Introduction

## Workflow

```mermaid
graph TD
A(Checkout Code)
B(Build Image)
C(Deploy to Staging)
D(Check Successful Metrics)
E{Successful?}
F(Deploy to Production)
G(Rollback)
H(Notify Successful Deploy)
I(Set Deployment Marker)
J(Notify Failed Deploy)

A --> B --> C -->|After 3 Minutes| D --> E -->|YES| F
B -->|Retry 3 times| B
C -->|Timeout 2 minutes| C
E -->|NO| G
G --> J
F --> H
F --> I
```

## Step0

What would it look like with a very naive simple Python.

```bash
make run-step-0
```

## Step1

What would it normally look like in the real world? queues or DB persistency with workers, state management, retries, etc.

## Step2

A rewrite of step0 with Python's async io, still naive

```bash
make run-step-2
```

## Step3

A Temporal Example

### Run Temporal

```bash
make start-temporal
```

### Run Temporal Workers

```bash
make start-workers
```

### Execute Workflow

```bash
make run-step-3
```
