
# Create AWS Lambda deployment files
serverless_yml = '''service: greenfuel-ml-api

frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    PYTHONPATH: /opt/python:/var/runtime
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
          Resource: "*"

functions:
  predict:
    handler: app.predict_handler
    events:
      - http:
          path: predict
          method: post
          cors: true
    timeout: 60
    memorySize: 512
    layers:
      - arn:aws:lambda:us-east-1:ACCOUNT_ID:layer:python-dependencies:1

  health:
    handler: app.health_handler
    events:
      - http:
          path: health
          method: get
          cors: true

  modelInfo:
    handler: app.model_info_handler
    events:
      - http:
          path: model-info
          method: get
          cors: true

  batchPredict:
    handler: app.batch_predict_handler
    events:
      - http:
          path: batch-predict
          method: post
          cors: true
    timeout: 120
    memorySize: 1024

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
    useDownloadCache: true
    useStaticCache: true
'''

with open('greenfuel-ml-frontend/serverless.yml', 'w') as f:
    f.write(serverless_yml)

print("✓ Created serverless.yml")

# Create AWS SAM template
sam_template = '''AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: GreenFuel-ML Hydrogen Production Prediction API

Globals:
  Function:
    Timeout: 60
    MemorySize: 512
    Runtime: python3.9
    Environment:
      Variables:
        TABLE_NAME: !Ref PredictionsTable

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - prod
    Description: Environment name

Resources:
  # Lambda Functions
  PredictFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub 'greenfuel-predict-${Environment}'
      CodeUri: .
      Handler: app.predict
      Events:
        PredictAPI:
          Type: Api
          Properties:
            RestApiId: !Ref API
            Path: /predict
            Method: post
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref PredictionsTable
      Layers:
        - !Ref DependenciesLayer

  HealthCheckFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub 'greenfuel-health-${Environment}'
      CodeUri: .
      Handler: app.health
      Events:
        HealthAPI:
          Type: Api
          Properties:
            RestApiId: !Ref API
            Path: /health
            Method: get

  ModelInfoFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub 'greenfuel-modelinfo-${Environment}'
      CodeUri: .
      Handler: app.model_info
      Events:
        ModelInfoAPI:
          Type: Api
          Properties:
            RestApiId: !Ref API
            Path: /model-info
            Method: get

  # API Gateway
  API:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub 'greenfuel-api-${Environment}'
      StageName: !Ref Environment
      Cors:
        AllowMethods: "'GET,POST,OPTIONS'"
        AllowHeaders: "'Content-Type,Authorization'"
        AllowOrigin: "'*'"

  # Lambda Layer for Dependencies
  DependenciesLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub 'greenfuel-dependencies-${Environment}'
      Description: Python dependencies for GreenFuel-ML
      Content:
        S3Bucket: !Ref DependenciesBucket
        S3Key: layer.zip
      CompatibleRuntimes:
        - python3.9

  # S3 Bucket for dependencies
  DependenciesBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'greenfuel-dependencies-${Environment}-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled

  # DynamoDB Table for predictions history
  PredictionsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub 'greenfuel-predictions-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PredictionID
          AttributeType: S
        - AttributeName: Timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: PredictionID
          KeyType: HASH
        - AttributeName: Timestamp
          KeyType: RANGE
      TTL:
        AttributeName: ExpirationTime
        Enabled: true
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES

  # CloudWatch Log Group
  APILogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/greenfuel-${Environment}'
      RetentionInDays: 14

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub 'https://${API}.execute-api.${AWS::Region}.amazonaws.com/${Environment}'
    Export:
      Name: !Sub 'greenfuel-api-endpoint-${Environment}'

  PredictionsTableName:
    Description: DynamoDB table for predictions
    Value: !Ref PredictionsTable
    Export:
      Name: !Sub 'greenfuel-table-${Environment}'
'''

with open('greenfuel-ml-frontend/template.yaml', 'w') as f:
    f.write(sam_template)

print("✓ Created template.yaml (AWS SAM)")
