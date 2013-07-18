define [], ->
  'count':
    label: '#'
    title: 'Total number of tests'
  'errorsCombined':
    label: '#ERR'
    title: 'Total number of all errors combined'
  'errorsAborted':
    label: '#ABRTD'
    title: 'Error: Numer of times the navigation aborted,i.e. 
      simple_action_client.get_state() returned ABORTED'
  'errorsFailed':
    label: '#FLD'
    title: 'Error: Numer of times the navigation failed, i.e. 
      simple_action_client.get_state() did neither return SUCCEEDED nor 
      ABORTED'
  'errorsMissed':
    label: '#MISS'
    title: 'Error: Number of time the navigation returned success but the 
      actual position did not match the goal position'
  'errorsTimedout':
    label: '#TO'
    title: 'Error: Number of times the navigation timed out'
  'mean.collisions':
    label: '#Col'
    title: 'Number of collisions'
  'robot':
    label: 'Roboter'
    title: 'The robot used in the simulation'
  'navigation':
    label: 'Navigation'
    title: 'The navigation used in the simulation'
  'scenario':
    label: 'Scenario'
    title: 'The scenarion used in the simulation'
  'mean.duration':
    label: 'Duration'
    title: 'Duration &empty; in s'
    formatter: 'float'
  'mean.distance':
    label: 'Distance'
    title: 'Distance the robot moved &empty; in m'
    formatter: 'float'
  'mean.rotation':
    label: 'Rotation'
    title: 'Number of degree the robot rotated &empty; in deg'
    formatter: 'float'
