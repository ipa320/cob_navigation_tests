(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["applicationDev.js"] = function(__obj) {
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
        __out.push('(function() {\n  this.ecoTemplates || (this.ecoTemplates = {});\n  this.ecoTemplates["applicationDev"] = function(__obj) {\n    if (!__obj) __obj = {};\n    var __out = [], __capture = function(callback) {\n      var out = __out, result;\n      __out = [];\n      callback.call(this);\n      result = __out.join(\'\');\n      __out = out;\n      return __safe(result);\n    }, __sanitize = function(value) {\n      if (value && value.ecoSafe) {\n        return value;\n      } else if (typeof value !== \'undefined\' && value != null) {\n        return __escape(value);\n      } else {\n        return \'\';\n      }\n    }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;\n    __safe = __obj.safe = function(value) {\n      if (value && value.ecoSafe) {\n        return value;\n      } else {\n        if (!(typeof value !== \'undefined\' && value != null)) value = \'\';\n        var result = new String(value);\n        result.ecoSafe = true;\n        return result;\n      }\n    };\n    if (!__escape) {\n      __escape = __obj.escape = function(value) {\n        return (\'\' + value)\n          .replace(/&/g, \'&amp;\')\n          .replace(/</g, \'&lt;\')\n          .replace(/>/g, \'&gt;\')\n          .replace(/"/g, \'&quot;\');\n      };\n    }\n    (function() {\n      (function() {\n        __out.push(\'<div class="chartContainer navigation"></div>\\n<div class="chartContainer robot"></div>\\n\');\n      \n      }).call(this);\n      \n    }).call(__obj);\n    __obj.safe = __objSafe, __obj.escape = __escape;\n    return __out.join(\'\');\n  };\n}).call(this);\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
