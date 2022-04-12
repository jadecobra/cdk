import boto3
import botocore.exceptions
import os

const url = require('url');


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
    return round(get_step_functions_base_cost() * (6 + n), 5)

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
    setLambdaPower(lambda_arn, value);
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

def invokeLambdaProcessor(processorARN, payload, preOrPost='Pre'):
    processorData = invokeLambda(processorARN, None, payload);
    if processorData.FunctionError:
        raise Exception(f'{preOrPost}Processor {processorARN} failed with error {processorData.Payload} and payload {payload}');
    return processorData.Payload

/**
 * Wrapper around Lambda function invocation with pre/post-processor functions.
 */
module.exports.invokeLambdaWithProcessors = async(lambda_arn, alias, payload, preARN, postARN) => {

    var actualPayload = payload; // might change based on pre-processor

    // first invoke pre-processor, if provided
    if (preARN) {
        console.log('Invoking pre-processor');
        // overwrite payload with pre-processor's output (only if not empty)
        const preProcessorOutput = await utils.invokeLambdaProcessor(preARN, payload, 'Pre');
        if (preProcessorOutput) {
            actualPayload = preProcessorOutput;
        }
    }

    // invoke function to be power-tuned
    const invocationResults = await utils.invokeLambda(lambda_arn, alias, actualPayload);

    // then invoke post-processor, if provided
    if (postARN) {
        console.log('Invoking post-processor');
        // note: invocation may have failed (invocationResults.FunctionError)
        await utils.invokeLambdaProcessor(postARN, invocationResults.Payload, 'Post');
    }

    return {
        actualPayload,
        invocationResults,
    };
};

/**
 * Invoke a given Lambda Function:Alias with payload and return its logs.
 */
module.exports.invokeLambda = (lambda_arn, alias, payload) => {
    console.log(`Invoking function ${lambda_arn}:${alias || '$LATEST'} with payload ${JSON.stringify(payload)}`);
    const params = {
        FunctionName: lambda_arn,
        Qualifier: alias,
        Payload: payload,
        LogType: 'Tail', // will return logs
    };
    const lambda = get_lambda_client_from_arn(lambda_arn);
    return lambda.invoke(params).promise();
};

/**
 * Fetch the body of an S3 object, given an S3 path such as s3://BUCKET/KEY
 */
module.exports.fetchPayloadFromS3 = async(s3Path) => {
    console.log('Fetch payload from S3', s3Path);

    if (typeof s3Path !== 'string' || s3Path.indexOf('s3://') === -1) {
        throw new Error('Invalid S3 path, not a string in the format s3://BUCKET/KEY');
    }

    const URI = url.parse(s3Path);
    URI.pathname = decodeURIComponent(URI.pathname || '');

    const bucket = URI.hostname;
    const key = URI.pathname.slice(1);

    if (!bucket || !key) {
        throw new Error(`Invalid S3 path: "${s3Path}" (bucket: ${bucket}, key: ${key})`);
    }

    const data = await utils._fetchS3Object(bucket, key);

    try {
        // try to parse into JSON object
        return JSON.parse(data);
    } catch (_) {
        // otherwise return as is
        return data;
    }


};

module.exports._fetchS3Object = async(bucket, key) => {
    const s3 = new AWS.S3();
    try {
        const response = await s3.getObject({
            Bucket: bucket,
            Key: key,
        }).promise();
        return response.Body.toString('utf-8');
    } catch (err) {
        if (err.statusCode === 403) {
            throw new Error(
                `Permission denied when trying to read s3://${bucket}/${key}. ` +
                'You might need to re-deploy the app with the correct payloadS3Bucket parameter.',
            );
        } else if (err.statusCode === 404) {
            throw new Error(
                `The object s3://${bucket}/${key} does not exist. ` +
                'Make sure you are trying to access an existing object in the correct bucket.',
            );
        } else {
            throw new Error(`Unknown error when trying to read s3://${bucket}/${key}. ${err.message}`);
        }
    }
};

/**
 * Generate a list of `num` payloads (repeated or weighted)
 */
module.exports.generatePayloads = (num, payloadInput) => {
    if (Array.isArray(payloadInput)) {
        // if array, generate a list of payloads based on weights

        // fail if empty list or missing weight/payload
        if (payloadInput.length === 0 || payloadInput.some(p => !p.weight || !p.payload)) {
            throw new Error('Invalid weighted payload structure');
        }

        if (num < payloadInput.length) {
            throw new Error(`You have ${payloadInput.length} payloads and only "num"=${num}. Please increase "num".`);
        }

        // we use relative weights (not %), so here we compute the total weight
        const total = payloadInput.map(p => p.weight).reduce((a, b) => a + b, 0);

        // generate an array of num items (to be filled)
        const payloads = utils.range(num);

        // iterate over weighted payloads and fill the array based on relative weight
        let done = 0;
        for (let i = 0; i < payloadInput.length; i++) {
            const p = payloadInput[i];
            var howMany = Math.floor(p.weight * num / total);
            if (howMany < 1) {
                throw new Error('Invalid payload weight (num is too small)');
            }

            // make sure the last item fills the remaining gap
            if (i === payloadInput.length - 1) {
                howMany = num - done;
            }

            // finally fill the list with howMany items
            payloads.fill(utils.convertPayload(p.payload), done, done + howMany);
            done += howMany;
        }

        return payloads;
    } else {
        // if not an array, always use the same payload (still generate a list)
        const payloads = utils.range(num);
        payloads.fill(utils.convertPayload(payloadInput), 0, num);
        return payloads;
    }
};

/**
 * Convert payload to string, if it's not a string already
 */
module.exports.convertPayload = (payload) => {
    /**
     * Return true only if the input is a JSON-encoded string.
     * For example, '"test"' or '{"key": "value"}'.
     */
    const isJsonString = (s) => {
        if (typeof s !== 'string')
            return false;

        try {
            JSON.parse(s);
        } catch (e) {
            return false;
        }
        return true;
    };

    // optionally convert everything into string
    if (typeof payload !== 'undefined' && !isJsonString(payload)) {
        // note: 'just a string' becomes '"just a string"'
        console.log('Converting payload to JSON string from ', typeof payload);
        payload = JSON.stringify(payload);
    }
    return payload;
};

/**
 * Compute average price, given average duration.
 */
module.exports.computePrice = (minCost, minRAM, value, duration) => {
    // it's just proportional to ms (ceiled) and memory value
    return Math.ceil(duration) * minCost * (value / minRAM);
};

module.exports.parseLogAndExtractDurations = (data) => {
    return data.map(log => {
        const logString = utils.base64decode(log.LogResult || '');
        return utils.extractDuration(logString);
    });
};

/**
 * Compute total cost
 */
module.exports.computeTotalCost = (minCost, minRAM, value, durations) => {
    if (!durations || !durations.length) {
        return 0;
    }

    // compute corresponding cost for each durationo
    const costs = durations.map(duration => utils.computePrice(minCost, minRAM, value, duration));

    // sum all together
    return costs.reduce((a, b) => a + b, 0);
};

/**
 * Copute average duration
 */
module.exports.computeAverageDuration = (durations) => {
    if (!durations || !durations.length) {
        return 0;
    }

    // 20% of durations will be discarted (trimmed mean)
    const toBeDiscarded = parseInt(durations.length * 20 / 100, 10);

    const newN = durations.length - 2 * toBeDiscarded;

    // compute trimmed mean (discard 20% of low/high values)
    const averageDuration = durations
        .sort(function(a, b) { return a - b; }) // sort numerically
        .slice(toBeDiscarded, -toBeDiscarded) // discard first/last values
        .reduce((a, b) => a + b, 0) // sum all together
        / newN
    ;

    return averageDuration;
};

/**
 * Extract duration (in ms) from a given Lambda's CloudWatch log.
 */
module.exports.extractDuration = (log) => {
    // extract duration from log (anyone can suggest a regex?)
    const durationSplit = log.split('\tDuration: ');
    if (durationSplit.length < 2) return 0;

    const durationStr = durationSplit[1].split(' ms')[0];
    return parseFloat(durationStr);
};

/**
 * Encode a given string to base64.
 */
module.exports.base64decode = (str) => {
    return Buffer.from(str, 'base64').toString();
};

/**
 * Generate a list of size n.
 */
module.exports.range = (n) => {
    if (n === null || typeof n === 'undefined') {
        n = -1;
    }
    return Array.from(Array(n).keys());
};

module.exports.regionFromARN = (arn) => {
    if (typeof arn !== 'string' || arn.split(':').length !== 7) {
        throw new Error('Invalid ARN: ' + arn);
    }
    return arn.split(':')[3];
};

module.exports.lambdaClientFromARN = (lambda_arn) => {
    const region = this.regionFromARN(lambda_arn);
    return new AWS.Lambda({region});
};

/**
 * Generate a URL with encoded stats.
 * Note: the URL hash is never sent to the server.
 */
module.exports.buildVisualizationURL = (stats, baseURL) => {

    function encode(inputList, EncodeType = null) {
        EncodeType = EncodeType || Float32Array;
        inputList = new EncodeType(inputList);
        inputList = new Uint8Array(inputList.buffer);
        return Buffer.from(inputList).toString('base64');
    }

    // sort by power
    stats.sort((p1, p2) => {
        return p1.power - p2.power;
    });

    const sizes = stats.map(p => p.power);
    const times = stats.map(p => p.duration);
    const costs = stats.map(p => p.cost);

    const hash = [
        encode(sizes, Int16Array),
        encode(times),
        encode(costs),
    ].join(';');

    return baseURL + '#' + hash;
};

/**
 * Using the prices supplied,
 * to figure what the base price is for the
 * supplied region.
 */
module.exports.baseCostForRegion = (priceMap, region) => {
    if (priceMap[region]) {
        return priceMap[region];
    }
    console.log(region + ' not found in base price map, using default: ' + priceMap['default']);
    return priceMap['default'];
};
