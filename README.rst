===========================
cloudformation-dynamodb-ttl
===========================

As of this writing, CloudFormation does not yet have native support for DynamoDB TTL.
This custom resource provider will allow you to work around this gap and set TTL
configurations for your DynamoDB tables from within your CloudFormation templates.

Deployment
----------

1. Create versioned S3 Bucket.
2. Deploy ``codebuild.yml`` CloudFormation template.
3. Execute a build of the generated CodeBuild project.

    The Name and Arn of the built project are exported as CloudFormation cross-stack values.
        * **DynamoDBTTLBuildProjectName**
        * **DynamoDBTTLBuildProjectArn**

4. Deploy ``providers.yml`` CloudFormation template.

Usage
-----

The provided CloudFormation template exports the Arn of the Lambda provider:
    * **DynamoDBTTLProvider**

The provider accepts inputs exactly as expected in the `UpdateTimeToLive`_ API call.

.. code-block:: yaml

    Resources:
        ExampleTable:
            Type: AWS::DynamoDB::Table
            Properties:
                AttributeDefinitions:
                    -
                        AttributeName: ExKey
                        AttributeType: S
                KeySchema:
                    -
                        AttributeName: ExKey
                        KeyType: HASH
                ProvisionedThroughput:
                    ReadCapacityUnits: 1
                    WriteCapacityUnits: 1
        ExampleTableTTL:
            Type: Custom::DynamoDBTTL
            Properties:
                ServiceToken: !ImportValue DynamoDBTTLProvider
                TableName: !Ref ExampleTable
                TimeToLiveSpecification:
                    Enabled: True
                    AttributeName: ExTimeStampAttribute


.. _UpdateTimeToLive: http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateTimeToLive.html