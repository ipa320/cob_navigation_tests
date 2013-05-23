define [], ()->
  formatDate: ( timestamp )->
    date = new Date( timestamp )
    "#{date.getDate()}-#{date.getMonth()}-#{date.getFullYear()}"
    
