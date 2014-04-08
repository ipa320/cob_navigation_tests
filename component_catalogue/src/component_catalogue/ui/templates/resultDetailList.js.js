(function() {
  this.ecoTemplates || (this.ecoTemplates = {});
  this.ecoTemplates["resultDetailList.js"] = function(__obj) {
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
        __out.push('(function() {\n  this.ecoTemplates || (this.ecoTemplates = {});\n  this.ecoTemplates["resultDetailList"] = function(__obj) {\n    if (!__obj) __obj = {};\n    var __out = [], __capture = function(callback) {\n      var out = __out, result;\n      __out = [];\n      callback.call(this);\n      result = __out.join(\'\');\n      __out = out;\n      return __safe(result);\n    }, __sanitize = function(value) {\n      if (value && value.ecoSafe) {\n        return value;\n      } else if (typeof value !== \'undefined\' && value != null) {\n        return __escape(value);\n      } else {\n        return \'\';\n      }\n    }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;\n    __safe = __obj.safe = function(value) {\n      if (value && value.ecoSafe) {\n        return value;\n      } else {\n        if (!(typeof value !== \'undefined\' && value != null)) value = \'\';\n        var result = new String(value);\n        result.ecoSafe = true;\n        return result;\n      }\n    };\n    if (!__escape) {\n      __escape = __obj.escape = function(value) {\n        return (\'\' + value)\n          .replace(/&/g, \'&amp;\')\n          .replace(/</g, \'&lt;\')\n          .replace(/>/g, \'&gt;\')\n          .replace(/"/g, \'&quot;\');\n      };\n    }\n    (function() {\n      (function() {\n        var colData, columnData, columnKey, i, row, _ref, _ref1, _ref2;\n      \n        __out.push(\'<div class="table-container details">\\n  <div class="detail"><a class="back" href="javascript:void(0)"><img src="/ui/assets/images/back.png" /></a>Test-Details for \');\n      \n        __out.push(__sanitize(this.title));\n      \n        __out.push(\'</div>\\n  <div class="table-detail-container">\\n    <table class="display" cellspacing="0" cellpadding="0">\\n    <thead>\\n        <tr>\\n            <th title="Select" class="checkbox">&nbsp;</th>\\n            <th title="Number">#</th>\\n            \');\n      \n        _ref = this.columns;\n        for (columnKey in _ref) {\n          colData = _ref[columnKey];\n          __out.push(\'\\n            <th title="\');\n          __out.push(colData.title);\n          __out.push(\'">\');\n          __out.push(colData.label);\n          __out.push(\'</th>\\n            \');\n        }\n      \n        __out.push(\'\\n        </tr>\\n    </thead>\\n    <tbody>\\n        \');\n      \n        _ref1 = this.data;\n        for (i in _ref1) {\n          row = _ref1[i];\n          __out.push(\'\\n        <tr id="\');\n          __out.push(__sanitize(row.id));\n          __out.push(\'" class="row testDetail">\\n            <td class="checkbox"><input type="checkbox" data-no="\');\n          __out.push(__sanitize(i));\n          __out.push(\'"/></td>\\n            <td>\');\n          __out.push(__sanitize(i));\n          __out.push(\'</td>\\n            \');\n          _ref2 = this.columns;\n          for (columnKey in _ref2) {\n            columnData = _ref2[columnKey];\n            __out.push(\'\\n                <td class="\');\n            __out.push(__sanitize(columnKey));\n            __out.push(\'">\');\n            __out.push(helper.format(row[columnKey], columnData.formatter));\n            __out.push(\'&nbsp;</td>\\n            \');\n          }\n          __out.push(\'\\n        </tr>\\n        \');\n        }\n      \n        __out.push(\'\\n    </tbody>\\n    </table>\\n  </div>\\n</div>\\n\');\n      \n      }).call(this);\n      \n    }).call(__obj);\n    __obj.safe = __objSafe, __obj.escape = __escape;\n    return __out.join(\'\');\n  };\n}).call(this);\n');
      
      }).call(this);
      
    }).call(__obj);
    __obj.safe = __objSafe, __obj.escape = __escape;
    return __out.join('');
  };
}).call(this);
