# Backend for the Elevenlabs Speech to Text AI agent

The example prompt is located in the *prompt.md* file.

===

## Endpoints

> GET /stats for visualization
> GET /apidocs for endpoint descriptions

===

## Elevenlabs setup

Create an **AI Agent** with the provided prompt.

Create two custom webhooks for the agent to call.
Use the endpoint documentation for the webhook fields.
The call_id isshould be passed from the *conversation_id* dynamic variable.

===

## Container setup
The actual container canbe hosted anywhere, e.g heroku, ecs, etc.
If using heroku, remember to buld for *amd64*, not arm.
