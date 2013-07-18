define( [ 'ecoHelper' ], function( helper ){(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["resultDetailList"] = function(__obj) {
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
        var colData, columnData, columnKey, i, row, _ref, _ref1, _ref2;
      
        __out.push('<div class="table-container details">\n  <div class="detail"><a class="back" href="javascript:void(0)"><img src="/ui/assets/images/back.png" /></a>Test-Details for ');
      
        __out.push(__sanitize(this.title));
      
        __out.push('</div>\n  <div class="table-detail-container">\n    <table class="display" cellspacing="0" cellpadding="0">\n    <thead>\n        <tr>\n            ');
      
        _ref = this.columns;
        for (columnKey in _ref) {
          colData = _ref[columnKey];
          __out.push('\n            <th title="');
          __out.push(colData.title);
          __out.push('">');
          __out.push(colData.label);
          __out.push('</th>\n            ');
        }
      
        __out.push('\n        </tr>\n    </thead>\n    <tbody>\n        ');
      
        _ref1 = this.data;
        for (i in _ref1) {
          row = _ref1[i];
          __out.push('\n        <tr id="');
          __out.push(__sanitize(row.id));
          __out.push('" class="row">\n            ');
          _ref2 = this.columns;
          for (columnKey in _ref2) {
            columnData = _ref2[columnKey];
            __out.push('\n                <td class="');
            __out.push(__sanitize(columnKey));
            __out.push('">');
            __out.push(helper.format(row[columnKey], columnData.formatter));
            __out.push('&nbsp;</td>\n            ');
          }
          __out.push('\n        </tr>\n        ');
        }
      
        __out.push('\n    </tbody>\n    </table>\n  </div>\n</div>\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
return this.ecoTemplates[ 'resultDetailList' ];});