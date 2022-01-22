action_that_produces_variables = ActionThatProducesVariables(
    action_name='actionThatProducesVariables',
)
OtherAction(
    config=action_that_produces_variables.name_of_variable,
    action_name='otherAction'
)

# how to create a variable namespace
action_that_produces_variables = ActionThatProducesVariables(
    variables_namespace='VariableNamespace',
    actions_name='actioName'
)

# how to use global variables
action_that_produces_variables(
    config=codepipeline.GlobalVariables.execution_id,
    action_name='actionName'
)