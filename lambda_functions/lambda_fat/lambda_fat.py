def get_query_string_parameter(event=None, parameter=None):
    try:
        return int(event["queryStringParameters"][parameter])
    except KeyError:
        return 0

def get_first_number(event):
    return get_query_string_parameter(event, parameter='firstNumber')

def get_second_number(event):
    return get_query_string_parameter(event, parameter='secondNumber')

def add(event, context):
    return {
        'body': get_first_number(event) + get_second_number(event),
        'statusCode': 200
    }


def subtract(event, context):
    return {
        'body': get_first_number(event) - get_second_number(event),
        'statusCode': 200
    }

def multiply(event, context):
    return {
        'body': get_first_number(event) * get_second_number(event),
        'statusCode': 200
    }