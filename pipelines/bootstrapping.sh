env CDK_NEW_BOOTSTRAP=1

# how to bootstrap an environment for provisioning a pipeline
npx cdk bootstrap --profile admin-profile-1 --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess aws://123456789012/us-east-1

# how to bootstrap a different environment for deploying applications using pipeline in 123456789012
npx cdk bootstrap --profile admin-profile-2 --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust 123456789012 aws://234567890121/us-east-2

# how to trust an account to do lookups
npx cdk bootstrap --profile admin-profile-2 --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust-for-lookup 123456789012 aws://234567890121/us-east-2