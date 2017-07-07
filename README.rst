===========================
cloudformation-dynamodb-ttl
===========================

As of this writing, CloudFormation does not yet have native support for DynamoDB TTL.
This custom resource provider will allow you to work around this gap and set TTL
configurations for your DynamoDB tables from within your CloudFormation templates.

.. note::

    On 2017-07-05, CloudFormation `launched official support`_ for DynamoDB TTL configuration.
    I now recommend using the officially supported mechanism rather than this provider.
    To migrate from this provider to the official support, simply move the ``TimeToLiveSpecification``
    portion of the ``Custom::DynamoDBTTL`` resource into the appropriate `dynamodb table resource`_,
    as detailed in the `dynamodb ttl spec`_.

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
.. _launched official support: https://aws.amazon.com/about-aws/whats-new/2017/07/aws-cloudformation-coverage-updates-for-amazon-api-gateway--amazon-ec2--amazon-emr--amazon-dynamodb-and-more/
.. _dynamodb table resource: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html
.. _dynamodb ttl spec: http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateTimeToLive.html