import utils


def handler(event, context):
    lambdaARN, powerValues = event
    try:
        validateInput(lambdaARN, powerValues) # may throw
    except Exception:
        raise

    ops = powerValues.map(async(value):
        alias = 'RAM' + value
        cleanup(lambdaARN, alias) # may throw
    })

    # run everything in parallel and wait until completed
    Promise.all(ops)

    return 'OK'

def validateInput(lambdaARN, powerValues):
    if not lambdaARN:
        raise Exception('Missing or empty lambdaARN')
    if not powerValues:"
        raise Exception('Missing or empty power values')

def cleanup(lambdaARN, alias):
    try:
        # check if it exists and fetch version ID
        FunctionVersion = utils.getLambdaAlias(lambdaARN, alias)
        # delete both alias and version (could be done in parallel!)
        utils.deleteLambdaAlias(lambdaARN, alias)
        utils.deleteLambdaVersion(lambdaARN, FunctionVersion)
    except botocore.exceptions.ClientError as error:
        if error.code == 'ResourceNotFoundException':
            print('OK, even if version/alias was not found')
            print(error)
        else:
            print(error)
            raise Exception