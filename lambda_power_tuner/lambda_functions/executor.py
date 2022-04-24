import boto3
import os

# the executor needs a longer socket timeout to invoke long-running functions
# 15 minutes is fine here because the Executor will timeout anyway
AWS.config.update({httpOptions: {timeout: 15 * 60 * 1000}})

minRAM = parseInt(os.environ.get(minRAM, 10)

def handler(event, context):
    '''
    Execute the given function N times in series or in parallel.
    Then compute execution statistics (averate cost and duration).
    '''
    # read input from event
    {
        lambdaARN,
        value,
        num,
        enableParallel,
        payload,
        dryRun,
        preProcessorARN,
        postProcessorARN,
    } = extractDataFromInput(event)

    validateInput(lambdaARN, value, num) # may throw

    # force only 1 execution if dryRun
    if (dryRun):
        print('[Dry-run] forcing num=1')
        num = 1

    lambdaAlias = 'RAM' + value
    results

    # fetch architecture from $LATEST
    architecture = utils.getLambdaArchitecture(lambdaARN)
    print(f'Detected architecture type: {architecture}')

    # pre-generate an array of N payloads
    payloads = utils.generatePayloads(num, payload)

    if (enableParallel) {
        results = runInParallel(num, lambdaARN, lambdaAlias, payloads, preProcessorARN, postProcessorARN)
    } else {
        results = runInSeries(num, lambdaARN, lambdaAlias, payloads, preProcessorARN, postProcessorARN)
    }

    # get base cost for Lambda
    baseCost = utils.lambdaBaseCost(utils.regionFromARN(lambdaARN), architecture)

    return computeStatistics(baseCost, results, value)


validateInput = (lambdaARN, value, num):
    if (!lambdaARN) {
        raise Exception('Missing or empty lambdaARN')
    }
    if (!value or isNaN(value)) {
        raise Exception('Invalid value: ' + value)
    }
    if (!num or isNaN(num)) {
        raise Exception('Invalid num: ' + num)
    }


extractPayloadValue(input):
    if (input.payloadS3) {
        return utils.fetchPayloadFromS3(input.payloadS3) # might throw if access denied or 404
    } else if (input.payload) {
        return input.payload
    }
    return null


extractDataFromInput(event):
    input = event.input # original state machine input
    payload = extractPayloadValue(input)
    return {
        value: parseInt(event.value, 10),
        lambdaARN: input.lambdaARN,
        num: parseInt(input.num, 10),
        enableParallel: !!input.parallelInvocation,
        payload: payload,
        dryRun: input.dryRun == true,
        preProcessorARN: input.preProcessorARN,
        postProcessorARN: input.postProcessorARN,
    }
}

runInParallel(num, lambdaARN, lambdaAlias, payloads, preARN, postARN):
    results = []
    # run all invocations in parallel ...
    invocations = utils.range(num).map(async(_, i):
        {invocationResults, actualPayload} = utils.invokeLambdaWithProcessors(lambdaARN, lambdaAlias, payloads[i], preARN, postARN)
        # invocation errors return 200 and contain FunctionError and Payload
        if (invocationResults.FunctionError) {
            raise Exception(f'Invocation error (running in parallel): {invocationResults.Payload} with payload {JSON.stringify(actualPayload)}f')
        }
        results.push(invocationResults)
    })
    # ... and wait for results
    Promise.all(invocations)
    return results
}

runInSeries(num, lambdaARN, lambdaAlias, payloads, preARN, postARN):
    results = []
    for (i = 0 i < num i++) {
        # run invocations in series
        {invocationResults, actualPayload} = utils.invokeLambdaWithProcessors(lambdaARN, lambdaAlias, payloads[i], preARN, postARN)
        # invocation errors return 200 and contain FunctionError and Payload
        if (invocationResults.FunctionError) {
            raise Exception(f'Invocation error (running in series): {invocationResults.Payload} with payload {JSON.stringify(actualPayload)}f')
        }
        results.push(invocationResults)
    }
    return results
}

computeStatistics = (baseCost, results, value):
    # use results (which include logs) to compute average duration ...

    durations = utils.parseLogAndExtractDurations(results)

    averageDuration = utils.computeAverageDuration(durations)
    print('Average duration: ', averageDuration)

    # ... and overall statistics
    averagePrice = utils.computePrice(baseCost, minRAM, value, averageDuration)

    # .. and total cost (exact $)
    totalCost = utils.computeTotalCost(baseCost, minRAM, value, durations)

    stats = {
        averagePrice,
        averageDuration,
        totalCost,
        value,
    }

    print('Stats: ', stats)
    return stats
}
