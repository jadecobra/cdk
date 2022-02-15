def extract_parameters(event):
    try:
        first_num = event["queryStringParameters"]['firstNumber']
    except KeyError:
        first_num = 0

    try:
        second_num = event["queryStringParameters"]['secondNumber']
    except KeyError:
        second_num = 0

    return first_num, second_num


def add(event, context):
    first_num, second_num = extract_parameters(event)

    result = int(first_num) + int(second_num)
    print("The result of % s + % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}


def subtract(event, context):
    first_num, second_num = extract_parameters(event)

    result = int(first_num) - int(second_num)
    print("The result of % s - % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}


def multiply(event, context):
    first_num, second_num = extract_parameters(event)

    result = int(first_num) * int(second_num)
    print("The result of % s * % s = %s" % (first_num, second_num, result))
    return {'body': result, 'statusCode': 200}
