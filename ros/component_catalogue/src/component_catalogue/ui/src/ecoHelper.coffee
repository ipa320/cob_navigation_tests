define [], ()->
  formatDate: ( timestamp )->
    date = new Date( timestamp )
    "#{date.getDate()}-#{date.getMonth()}-#{date.getFullYear()}"
    

  isNumber: ( num )->
    return !isNaN +num

  formatDecimals: ( num, decimals )->
    fac = Math.pow 10, decimals
    return Math.round( +num*fac )/fac

