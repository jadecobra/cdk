import boto3
import botocore.exceptions
import os

url = require('url')
s3 = new AWS.S3()


def get_base_cost_for_region(price_map, region):
    return price_map.get(region, price_map['default'])

def get_lambda_function_base_cost(region=None, architecture=None):
    prices = os.environ['baseCosts']
    try:
        price_map = prices[architecture]
    except KeyError:
        raise Exception(f'Unsupported Architecture: {architecture}')
    return get_base_cost_for_region(price_map, region)

def get_step_functions_base_cost():
    return get_base_cost_for_region(os.environ['sfCosts'], os.environ['region'])

def get_step_functions_cost(n):
    return round(get_step_functions_base_cost() # (6 + n), 5)

def all_power_values():
    return (number for number in range(128, 3008, 64))

def get_lambda_client_from_arn(lambda_arn):
    return

def get_lambda_alias(lambda_arn=None, alias=None):
    print('Checking alias ', alias)
    return get_lambda_client_from_arn(lambda_arn).get_alias(
        FunctionName=lambda_arn,
        Name=alias,
    )

def alias_exists(lambda_arn=None, alias=None):
    try:
        get_lambda_alias(lambda_arn, alias)
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise
    else:
        return True

def setLambdaPower(lambda_arn=None, value=None):
    return waitForFunctionUpdate(lambda_arn)

def publishLambdaVersion(lambda_arn):
    return

def update_lambda_alias(lambda_arn=None, alias=None, version=None):
    return

def create_lambda_alias(lambda_arn=None, alias=None, version=None):
    return


def create_power_configuration(lambda_arn=None, value=None, alias=None):
    setLambdaPower(lambda_arn, value)
    {Version} = publishLambdaVersion(lambda_arn)
    if alias_exists(lambda_arn, alias):
        update_lambda_alias(lambda_arn, alias, Version)
    else:
        create_lambda_alias(lambda_arn, alias, Version)

def waitForFunctionUpdate(lambda_arn):
    print('Waiting for update to complete')
    return get_lambda_client_from_arn(lambda_arn).waitFor(
        'functionUpdated',
        {
            'FunctionName': lambda_arn,
            '$waiter': {
                'delay': 0.5,
            }
        }
    )

def getLambdaPower(lambda_arn):
    print('Getting current power value')
    config = get_lambda_client_from_arn(lambda_arn).get_function_configuration(
        FunctionName=lambda_arn,
        Qualifier='$LATEST',
    )
    return config.MemorySize

def getLambdaArchitecture(lambda_arn):
    print('Getting current architecture')
    config = get_lambda_client_from_arn(lambda_arn).get_function_configuration(
        FunctionName=lambda_arn,
        Qualifier='$LATEST',
    )
    if not config['Architectures']:
        return config['Architectures'][0]
    return 'x86_64'

def setLambdaPower(lambda_arn=None, value=None):
    print('Setting power to ', value)
    return get_lambda_client_from_arn(lambda_arn).update_function_configuration(
        FunctionName=lambda_arn,
        MemorySize=parseInt(value, 10),
    )

def publishLambdaVersion(lambda_arn):
    print('Publishing new version')
    return get_lambda_client_from_arn(lambda_arn).publish_version(FunctionName=lambda_arn)

def deleteLambdaVersion(lambda_arn=None, version=None):
    print('Deleting version ', version)
    get_lambda_client_from_arn(lambda_arn).deleteFunction(
        FunctionName=lambda_arn,
        Qualifier=version
    )

def createLambdaAlias(lambda_arn=None, alias=None, version=None):
    print('Creating Alias ', alias)
    return get_lambda_client_from_arn(lambda_arn).createAlias(
        FunctionName=lambda_arn,
        FunctionVersion=version,
        Name=alias,
    )

def updateLambdaAlias(lambda_arn=None, alias=None, version=None):
    print('Updating Alias ', alias)
    return get_lambda_client_from_arn(lambda_arn).updateAlias(
        FunctionName=lambda_arn,
        FunctionVersion=version,
        Name=alias
    )

def deleteLambdaAlias(lambda_arn=None, alias=None):
    print('Deleting alias ', alias)
    return get_lambda_client_from_arn(lambda_arn).deleteAlias(
        FunctionName=lambda_arn,
        Name=alias,
    )

def invokeLambdaProcessor(processorARN=None, payload=None, preOrPost='Pre'):
    processorData = invokeLambda(processorARN, None, payload)
    if processorData.FunctionError:
        raise Exception(f'{preOrPost}Processor {processorARN} failed with error {processorData.Payload} and payload {payload}')
    return processorData.Payload

def invokeLambdaWithProcessors(lambda_arn, alias, payload, preARN, postARN):
    actualPayload = payload
    if preARN:
        print('Invoking pre-processor')
        preProcessorOutput = invokeLambdaProcessor(preARN, payload, 'Pre')
        if preProcessorOutput:
            actualPayload = preProcessorOutput

    invocationResults = invokeLambda(lambda_arn, alias, actualPayload)

    if postARN:
        print('Invoking post-processor')
        invokeLambdaProcessor(postARN, invocationResults.Payload, 'Post')

    return {
        actualPayload,
        invocationResults,
    }

def invokeLambda(lambda_arn, alias, payload):
    '''
    Invoke a given Lambda Function:Alias with payload and return its logs.
    '''
    print(f'Invoking function {lambda_arn}:{alias or '$LATEST'} with payload {JSON.stringify(payload)}')
    return get_lambda_client_from_arn(lambda_arn).invoke(
        FunctionName=lambda_arn,
        Qualifier=alias,
        Payload=payload,
        LogType='Tail',
    )

def fetchPayloadFromS3(s3Path):
    """
    Fetch the body of an S3 object, given an S3 path such as s3://BUCKET/KEY
    """
    print('Fetch payload from S3', s3Path)

    if isinstance(s3Path, str) or s3Path.find('s3://') == -1:
        raise Exception('Invalid S3 path, not a string in the format s3://BUCKET/KEY')

    URI = url.parse(s3Path)
    URI.pathname = decodeURIComponent(URI.pathname or '')

    bucket = URI.hostname
    key = URI.pathname.slice(1)

    if not bucket or not key:
        raise Exception(f'Invalid S3 path: "{s3Path}" (bucket: {bucket}, key: {key})')

    data = fetchS3Object(bucket, key)

    try:
        return JSON.parse(data)
    except Exception:
        return data

def fetchS3Object(bucket, key):
    try:
        response = s3.getObject(
            Bucket=bucket,
            Key=key,
        )
        return str(response['Body']
    except botocore.exceptions.ClientError as error:
        if error['StatusCode'] == 403:
            raise Exception(
                f'Permission denied when trying to read s3://{bucket}/{key}. You might need to re-deploy the app with the correct payloadS3Bucket parameter.',
        elif error['statusCode'] == 404:
            raise Exception(
                f'The object s3://{bucket}/{key} does not exist. Make sure you are trying to access an existing object in the correct bucket.',
            )
        else:
            raise Exception(f'Unknown error when trying to read s3://{bucket}/{key}. {err.message}')

def generatePayloads(num, payloadInput):
    if isinstance(payloadInput, list):
        if len(payloadInput) == 0 or payloadInput.some(p => !p.weight or !p.payload)):
            raise Exception('Invalid weighted payload structure')

        if num < len(payloadInput):
            raise Exception(f'You have {payloadInput.length} payloads and only "num"={num}. Please increase "num".')

        total = payloadInput.map(p => p.weight).reduce((a, b) => a + b, 0)
        payloads = utils.range(num)

        # iterate over weighted payloads and fill the array based on relative weight
        done = 0
        for i in range(len(payloadInput)):
            p = payloadInput[i]
            howMany = Math.floor(p.weight # num / total)
            if howMany < 1:
                raise Exception('Invalid payload weight (num is too small)')

            if i == payloadInput.length - 1:
                howMany = num - done

            # finally fill the list with howMany items
            payloads.fill(utils.convertPayload(p.payload), done, done + howMany)
            done += howMany

        return payloads
    else:
        # if not an array, always use the same payload (still generate a list)
        payloads = utils.range(num)
        payloads.fill(utils.convertPayload(payloadInput), 0, num)
        return payloads

def convertPayload(payload):
    #
    # Return true only if the input is a JSON-encoded string.
    # For example, '"test"' or '{"key": "value"}'.
    #
    isJsonString(s):
        if not isinstance(s, 'string'):
            return false

        try:
            JSON.parse(s)
        except Exception:
            return false
        return true

    # optionally convert everything into string
    if not payload & not isJsonString(payload):
        # note: 'just a string' becomes '"just a string"'
        print('Converting payload to JSON string from ', type(payload))
        payload = JSON.stringify(payload)
    return payload

#
# Compute average price, given average duration.
#
def computePrice(minCost, minRAM, value, duration):
    # it's just proportional to ms (ceiled) and memory value
    return Math.ceil(duration // minCost // (value / minRAM))

def parseLogAndExtractDurations(data):
    return data.map(log => {
        logString = utils.base64decode(log.LogResult or '')
        return utils.extractDuration(logString)
    })

def computeTotalCost(minCost, minRAM, value, durations):
    if not durations or len(durations) == 0:
        return 0

    # compute corresponding cost for each durationo
    costs = durations.map(duration => utils.computePrice(minCost, minRAM, value, duration))

    # sum all together
    return costs.reduce((a, b) => a + b, 0)

def computeAverageDuration(durations):
    if not durations or len(durations):
        return 0

    # 20% of durations will be discarted (trimmed mean)
    toBeDiscarded = parseInt(len(durations) // 20 / 100, 10)

    newN = len(durations) - 2 // toBeDiscarded

    # compute trimmed mean (discard 20% of low/high values)
    averageDuration = durations
        .sort(function(a, b: return a - b ) # sort numerically
        .slice(toBeDiscarded, -toBeDiscarded) # discard first/last values
        .reduce((a, b) => a + b, 0) # sum all together
        / newN


    return averageDuration

def extractDuration(log):
    # extract duration from log (anyone can suggest a regex?)
    durationSplit = log.split('\tDuration: ')
    if len(durationSplit) < 2: return 0

    durationStr = durationSplit[1].split(' ms')[0]
    return parseFloat(durationStr)

def base64decode(str):
    return Buffer.from(str, 'base64').toString()

def range(n):
    if not n:
        n = -1
    return Array.from(Array(n).keys())

def regionFromARN(arn):
    if isinstance(arn, str) or len(arn.split(':')) != 7:
        raise Exception(f'Invalid ARN: {arn}')
    return arn.split(':')[3]

def lambdaClientFromARN(lambda_arn):
    return boto3.client('lambda', region_name=regionFromARN(lambda_arn))

def encode(inputList, EncodeType=None):
    EncodeType = EncodeType if EncodeType else Float32Array
    inputList = EncodeType(inputList)
    inputList = Uint8Array(inputList.buffer)
    return Buffer.from(inputList).toString('base64')

def buildVisualizationURL(stats, baseURL):
    # sort by power
    stats.sort((p1, p2):
        return p1.power - p2.power
    })

    sizes = stats.map(p => p.power)
    times = stats.map(p => p.duration)
    costs = stats.map(p => p.cost)

    hash = [
        encode(sizes, Int16Array),
        encode(times),
        encode(costs),
    ].join('')

    return baseURL + '#' + hash

def baseCostForRegion(priceMap, region):
    try:
        return priceMap[region]
    except KeyError:
        print(region, ' not found in base price map, using default: ', priceMap['default'])
        return priceMap['default']