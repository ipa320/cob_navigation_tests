define [], ()->
  formatDate: ( timestamp )->
    date = new Date( timestamp )
    "#{date.getDate()}-#{date.getMonth()}-#{date.getFullYear()}"

  playVideoFormatter: ( url )->
    src = $.trim url
    if src.indexOf( 'http://' ) != 0
      return "<span class=\"invalidVideo\">#{url}</span>"
    return "<a href=\"#{url}\">Play Video</a>"

    
  formatNiceDate: ( timestamp )->
    d_names = [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ]
    m_names = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
      "Oct", "Nov", "Dec" ]

    d = new Date( timestamp )
    curr_day  = d.getDay()
    curr_date = d.getDate()
    sup = ""
    switch curr_date
      when 1 or 21 or 31 then sup = 'st'
      when 2 or 22       then sup = 'nd'
      when 3 or 23       then sup = 'rd'
      else                    sup = 'nd'

    curr_month = d.getMonth()
    curr_year = d.getFullYear()

    return [
      d_names[ curr_day ],
      curr_date,
      #"<SUP>" + sup + "</SUP> ",
      m_names[curr_month],
      curr_year
    ].join( ' ' )

  isNumber: ( num )->
    return !isNaN +num

  formatDecimals: ( num, decimals )->
    fac = Math.pow 10, decimals
    return Math.round( +num*fac )/fac

  format: ( value, formatter )->
    if formatter == 'float'
      return @formatDecimals value, 2
    else if formatter == 'date'
      return @formatDate value
    else if formatter == 'niceDate'
      return @formatNiceDate value
    else if formatter == 'playVideo'
      return @playVideoFormatter value
    return value
