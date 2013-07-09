define( [ 'ecoHelper' ], function( helper ){(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["sortingOptions"] = function(__obj) {
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
        __out.push('<div class="sortingOptions">\n  <span class="intro">Sort Charts by:</span>\n  <input class="sort" type="radio" id="sortByDate" name="sorting" value="date" ');
      
        if (this.sorting === 'date') {
          __out.push(__sanitize("checked"));
        }
      
        __out.push('/><label for="sortByDate">Sort by date</label>\n  <input class="sort" type="radio" id="sortByDuration" name="sorting" value="duration" ');
      
        if (this.sorting === 'value') {
          __out.push(__sanitize("checked"));
        }
      
        __out.push(' /><label for="sortByDuration">Sort by duration</label>\n  <input class="sort" type="radio" id="sortByDistance" name="sorting" value="distance" ');
      
        if (this.sorting === 'value') {
          __out.push(__sanitize("checked"));
        }
      
        __out.push(' /><label for="sortByDistance">Sort by distance</label>\n  <input class="sort" type="radio" id="sortByRotation" name="sorting" value="rotation" ');
      
        if (this.sorting === 'value') {
          __out.push(__sanitize("checked"));
        }
      
        __out.push(' /><label for="sortByRotation">Sort by rotation</label>\n\n  <label for="showErrorsChkbx" class="showErrorsLabel">Show errors:</label><input type="checkbox" id="showErrorsChkbx" ');
      
        if (this.showErrors) {
          __out.push(__sanitize("checked"));
        }
      
        __out.push(' />\n</div>\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
return this.ecoTemplates[ 'sortingOptions' ];});