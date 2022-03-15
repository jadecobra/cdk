def case_1_handler(event, context):
    print('--- Approved transactions ---')
    print(event)

def case_2_handler(event, context):
    print('--- NY location transactions ---')
    print(event)

def case_3_handler(event, context):
    print('--- Unapproved transactions ---')
    print(event)