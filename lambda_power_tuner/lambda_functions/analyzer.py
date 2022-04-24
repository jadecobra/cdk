import os
import utils

visualizationURL = os.environ.get(visualizationURL)\
defaultStrategy = 'cost'
defaultBalancedWeight = 0.5
optimizationStrategies = {
    'cost': findCheapest,
    'speed': findFastest,
    'balanced': findBalanced,
}

def handler(event, context):
    '''Receive average cost and decide which power config wins.'''
    if not isinstance(event['stats'], list) or not len(event['stats']):
        raise Exception(f'Wrong input {event}')

    if event['dryRun']:
        return print('[Dry-run] Skipping analysis')

    return findOptimalConfiguration(event)

def getStrategy(event):
    # extract strategy name or fallback to default (cost)
    return event['strategy'] or defaultStrategy

def getBalancedWeight(event):
    # extract weight used by balanced strategy or fallback to default (0.5)
    weight = event['balancedWeight']
    if not weight:
        weight = defaultBalancedWeight
    # weight must be between 0 and 1
    return min(max(weight, 0.0), 1.0)

def findOptimalConfiguration(event):
    stats = extractStatistics(event)
    strategy = getStrategy(event)
    balancedWeight = getBalancedWeight(event)
    optimizationFunction = optimizationStrategies[strategy]()
    optimal = optimizationFunction(stats, balancedWeight)

    # also compute total cost of optimization state machine & lambda
    optimal.stateMachine = {}
    optimal.stateMachine['executionCost'] = utils.stepFunctionsCost(len(event['stats']))
    # optimal.stateMachine['lambdaCost'] = stats.map(p, p.totalCost).reduce((a, b), (a + b), 0) # fix this
    optimal.stateMachine['visualization'] = utils.buildVisualizationURL(stats, visualizationURL)

    # the total cost of the optimal branch execution is not needed
    del optimal.totalCost

    return optimal


def extractStatistics(event):
    # generate a list of objects with only the relevant data/stats
    return event['stats']
    # handle empty results from executor
    # fix this
        # .filter(stat => stat && stat.averageDuration)
        # .map(stat => ({
        #     power: stat.value,
        #     cost: stat.averagePrice,
        #     duration: stat.averageDuration,
        #     totalCost: stat.totalCost,
        # }))

def findCheapest(stats):
    print('Finding cheapest')

    // sort by cost
    stats.sort((p1, p2):
        if (p1.cost == p2.cost) {
            // return fastest if same cost
            return p1.duration - p2.duration
        }
        return p1.cost - p2.cost
    })

    print('Stats: ', stats)

    // just return the first one
    return stats[0]
}

findFastest = (stats):
    print('Finding fastest')

    // sort by duration/speed
    stats.sort((p1, p2):
        if (p1.duration == p2.duration) {
            // return cheapest if same speed
            return p1.cost - p2.cost
        }
        return p1.duration - p2.duration
    })

    print('Stats: ', stats)

    // just return the first one
    return stats[0]
}

findBalanced = (stats, weight):
    // choose a balanced configuration, weight is a number between 0 and 1 that express trade-off
    // between cost and time (0 = min time, 1 = min cost)
    print('Finding balanced configuration with balancedWeight = ', weight)


    // compute max cost and max duration
    maxCost = Math.max(...stats.map(x => x['cost']))
    maxDuration = Math.max(...stats.map(x => x['duration']))

    // formula for balanced value of a configuration ( value is minimized )
    getValue = x => weight * x['cost'] / maxCost + (1 - weight) * x['duration'] / maxDuration

    // sort stats by value
    stats.sort((x, y) => getValue(x) - getValue(y))

    print('Stats: ', stats)

    // just return the first one
    return stats[0]
}
