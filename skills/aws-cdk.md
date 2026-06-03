# Skill: AWS CDK

## Core principles
- Infrastructure is code — apply same quality standards as application code
- CDK stacks should be composable — use constructs to organise resources
- Never hardcode account IDs, region, or ARNs — use CDK context or environment variables
- Use CDK best practices — L2 constructs over L1 (CloudFormation) where available
- Destroy protection on production stacks — never allow accidental deletion

## Stack organisation
- One stack per service or bounded context
- Separate stacks for stateful (databases, queues) and stateless (Lambda, API Gateway) resources
- Share resources between stacks via SSM Parameter Store or Stack exports
- Never create cross-stack circular dependencies

## Lambda
- Set explicit memory and timeout per function — no default values in production
- Use environment variables for configuration — not hardcoded values
- Package only what Lambda needs — no bloated deployment packages
- Use Lambda layers for shared dependencies
- Enable X-Ray tracing for production functions
- Set reserved concurrency for critical functions
- Use Dead Letter Queue for async invocations
- Handler function must be thin — business logic in separate modules

## API Gateway
- Use RestApi or HttpApi — HttpApi for lower latency and cost
- Always use stages — dev, staging, prod
- Enable request validation at API Gateway level — not just in Lambda
- Use custom domain names — not generated API Gateway URLs in production
- Enable throttling to protect backend services
- Use API keys or Cognito for authentication — never open public endpoints without auth

## Security
- IAM roles follow least privilege — no wildcards in production
- No inline policies — use managed policies or construct grants
- Secrets in AWS Secrets Manager or SSM Parameter Store — never in CDK code
- VPC for resources that should not be publicly accessible
- Enable CloudTrail for audit logging

## Deployment
- Use CDK Pipelines for automated deployment — not manual cdk deploy in production
- Always run cdk diff before cdk deploy to review changes
- Deploy to staging first — never directly to production
- Tag all resources with environment, service, owner
- Use cdk synth to validate before deploy

## Common commands
- cdk synth          — synthesise CloudFormation template, validate stack
- cdk diff           — show what will change before deploying
- cdk deploy         — deploy stack
- cdk deploy --hotswap — fast deploy for Lambda code changes only (dev only)
- cdk destroy        — destroy stack (never in production without explicit approval)
- cdk ls             — list all stacks

## Restarting and redeploying services
- Lambda: cdk deploy --hotswap for code-only changes in development
- Lambda: cdk deploy for any infrastructure or configuration changes
- ECS service: cdk deploy triggers new deployment automatically
- To force restart without code change: update a dummy environment variable
- Never restart production services during business hours without change window
