define [], ->
  'date':
    label: 'Date'
    title: 'Date when the test was recorder ( not analysed )'
    formatter: 'niceDate'
  'error':
    label: 'Error Code'
    title: 'Possible errors:<br />timedout for when the test timed out<br /><br />aborted: when the navigation aborted the test e.g. because it could not find a path<br /><br />failed: if the navigation did neither abort nor succeed<br /><br />missed: if the navigation returned success but the goal position did not match the target position'
  'collisions':
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
  'duration':
    label: 'Duration'
    title: 'Duration in s'
    formatter: 'float'
  'distance':
    label: 'Distance'
    title: 'Distance the robot moved in m'
    formatter: 'float'
  'rotation':
    label: 'Rotation'
    title: 'Number of degree the robot rotated in deg'
    formatter: 'float'
  'video':
    label: 'Video'
    title: 'Watch a recorded video of the test if available'
    formatter: 'playVideo'
