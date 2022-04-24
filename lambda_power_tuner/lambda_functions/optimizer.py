import utils

def handler(event, context):
    '''Optionally auto-optimize based on the optimal power value.'''
    lambdaARN = event['lambdaARN']
    analysis = event['analysis']
    autoOptimize = event['autoOptimize']
    autoOptimizeAlias = event['autoOptimizeAlias']
    dryRun = event['dryRun']
    if analysis:
        optimalValue = analysis.power
    else:
        optimalValue = {}

    if dryRun:
        return print('[Dry-run] Not optimizing')

    validateInput(lambdaARN, optimalValue)

    if not autoOptimize:
        return print('Not optimizing')

    if not autoOptimizeAlias:
        # only update $LATEST power
        utils.setLambdaPower(lambdaARN, optimalValue)
    else:
        # create/update alias
        utils.createPowerConfiguration(lambdaARN, optimalValue, autoOptimizeAlias)

    return 'OK'

def validateInput(lambdaARN=None, optimalValue=None):
    if not lambdaARN:
        raise Exception('Missing or empty lambdaARN')
    if not optimalValue:
        raise Exception('Missing or empty optimal value')