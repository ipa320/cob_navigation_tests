define( [ 'ecoHelper' ], function( helper ){(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["textFilterRow"] = function(__obj) {
    if (!__obj) __obj = {};
    var __out = [], __capture = function(callback) {
      var out = __out, result;
      __out = [];
      callback.call(this);
      result = __out.join('');
      __out = out;
      return __safe(result);
    }, __sanitize = function(value) {
      if (value && value.ecoSafe) {
        return value;
      } else if (typeof value !== 'undefined' && value != null) {
        return __escape(value);
      } else {
        return '';
      }
    }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
    __safe = __obj.safe = function(value) {
      if (value && value.ecoSafe) {
        return value;
      } else {
        if (!(typeof value !== 'undefined' && value != null)) value = '';
        var result = new String(value);
        result.ecoSafe = true;
        return result;
      }
    };
    if (!__escape) {
      __escape = __obj.escape = function(value) {
        return ('' + value)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');
      };
    }
    (function() {
      (function() {
        __out.push('<div class="top">\n    <select class="filterField">\n        <option value="any">Any Field</option>\n        <option value="robot">Roboter</option>\n        <option value="navigation">Navigation</option>\n        <option value="scenario">Szenario</option>\n    </select>\n    <select class="filterType">\n        <option value="includes">includes</option>\n        <option value="excludes">excludes</option>\n    </select>\n</div>\n<div class="bottom">\n    <a class="expand" href="javascript:void(0)"><img src="assets/images/textFilterRow/expand.jpg" /></a>\n    <input type="text" class="filterValue" />\n    <a class="and" href="javascript:void(0)"><img src="assets/images/textFilterRow/and.jpg" /></a>\n    <a class="or" href="javascript:void(0)"><img src="assets/images/textFilterRow/or.jpg" /></a>\n    <span class="link"></span>\n</div>\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
return this.ecoTemplates[ 'textFilterRow' ];});