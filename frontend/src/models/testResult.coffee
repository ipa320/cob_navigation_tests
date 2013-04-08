define [ 'backbone' ], ( Backbone )-> 
  TestResult = Backbone.Model.extend
    defaults:
      duration:  null
      distance:  null
      rotation:  null
