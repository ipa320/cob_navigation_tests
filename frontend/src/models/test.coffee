define [ 'backbone' ], ( Backbone )-> 
  TestResult = Backbone.Model.extend
    defaults:
      date: 0
      robot: ''
      scenario: ''
      algorithm: ''
      tooSexy: 'yes'
      testResults: null
      duration:  null
      distance:  null
      rotation:  null
