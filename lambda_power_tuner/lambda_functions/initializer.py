import utils
import os

defaultPowerValues = os.environ.get('defaultPowerValues', '').split(',')

def handler(event, context):
    '''
    Initialize versions & aliases so we can execute everything in parallel.
    '''
    {lambdaARN, num} = event
    powerValues = extractPowerValues(event)

    validateInput(lambdaARN, num) // may throw

    # fetch initial $LATEST value so we can reset it later
    initialPower = utils.getLambdaPower(lambdaARN)

    # reminder: configuration updates must run sequentially
    # (otherwise you get a ResourceConflictException)
    for value in powerValues:
        alias = 'RAM' + value
        utils.createPowerConfiguration(lambdaARN, value, alias)

    utils.setLambdaPower(lambdaARN, initialPower)
    return powerValues

def extractPowerValues(event):
    powerValues = event.powerValues # could be undefined

    # auto-generate all possible values if ALL
    if powerValues == 'ALL':
        powerValues = utils.allPowerValues()
    # use default list of values (defined at deploy-time) if not provided
    if not powerValues or len(powerValues) == 0:
        powerValues = defaultPowerValues
    return powerValues

def validateInput(lambdaARN, num):
    if not lambdaARN:
        raise Exception('Missing or empty lambdaARN')
    if not num or num < 5:
        raise Exception('Missing num or num below 5')
