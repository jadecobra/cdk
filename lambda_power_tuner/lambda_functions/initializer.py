'use strict'

utils = require('./utils')
defaultPowerValues = process.env.defaultPowerValues.split(',')

/**
 * Initialize versions & aliases so we can execute everything in parallel.
 */
def handler(event, context):

    {lambdaARN, num} = event
    powerValues = extractPowerValues(event)

    validateInput(lambdaARN, num) // may throw

    // fetch initial $LATEST value so we can reset it later
    initialPower = utils.getLambdaPower(lambdaARN)

    // reminder: configuration updates must run sequentially
    // (otherwise you get a ResourceConflictException)
    for (value of powerValues){
        alias = 'RAM' + value
        utils.createPowerConfiguration(lambdaARN, value, alias)
    }

    utils.setLambdaPower(lambdaARN, initialPower)

    return powerValues
}

extractPowerValues = (event):
    powerValues = event.powerValues // could be undefined

    // auto-generate all possible values if ALL
    if (powerValues === 'ALL') {
        powerValues = utils.allPowerValues()
    }

    // use default list of values (defined at deploy-time) if not provided
    if (!powerValues || powerValues.length === 0) {
        powerValues = defaultPowerValues
    }

    return powerValues
}

validateInput = (lambdaARN, num):
    if (!lambdaARN) {
        raise Exception('Missing or empty lambdaARN')
    }
    if (!num || num < 5) {
        raise Exception('Missing num or num below 5')
    }
}
