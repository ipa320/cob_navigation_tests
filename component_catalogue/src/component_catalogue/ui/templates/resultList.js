define( [ 'ecoHelper' ], function( helper ){(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["resultList"] = function(__obj) {
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
        var columName, columnKey, columnLabel, row, _i, _len, _ref, _ref1, _ref2;
      
        __out.push('<div class="fixed-table-container">\n    <div class="header-background"></div>\n    <div class="table-inner">\n        <table class="display" cellspacing="0" cellpadding="0">\n        <thead>\n            <tr>\n                <th></th>\n                ');
      
        _ref = this.columns;
        for (columnKey in _ref) {
          columnLabel = _ref[columnKey];
          __out.push('\n                <th><div title="');
          __out.push(columnLabel[1]);
          __out.push('">');
          __out.push(columnLabel[0]);
          __out.push('</div></th>\n                ');
        }
      
        __out.push('\n            </tr>\n        </thead>\n        <tbody>\n            ');
      
        _ref1 = this.data;
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          row = _ref1[_i];
          __out.push('\n            <tr id="');
          __out.push(__sanitize(row.id));
          __out.push('" class="row">\n                ');
          if (row.selected) {
            __out.push('\n                    <td><input type="checkbox" class=="selected" checked="checked"/></td>\n                ');
          } else {
            __out.push('\n                    <td><input type="checkbox" class=="selected" /></td>\n                ');
          }
          __out.push('\n                ');
          _ref2 = this.columns;
          for (columnKey in _ref2) {
            columName = _ref2[columnKey];
            __out.push('\n                    <td>');
            if (helper.isNumber(row[columnKey])) {
              __out.push('\n                        ');
              __out.push(__sanitize(helper.formatDecimals(row[columnKey], 2)));
              __out.push('\n                    ');
            } else {
              __out.push('\n                        ');
              __out.push(__sanitize(row[columnKey]));
              __out.push('\n                    ');
            }
            __out.push('</td>\n                ');
          }
          __out.push('\n            </tr>\n            ');
        }
      
        __out.push('\n        <tbody>\n        </tbody>\n        </table>\n    </div>\n</div>\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
return this.ecoTemplates[ 'resultList' ];});