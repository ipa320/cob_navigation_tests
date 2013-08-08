// Generated by CoffeeScript 1.6.2
(function() {
  define(['backbone', 'jquery-tipTip', 'jquery.dataTables', 'templates/resultList', 'templates/resultDetailList', 'views/columnsResultList', 'views/columnsDetailResultList'], function(Backbone, tiptip, dataTables, resultListTmpl, resultDetailListTmpl, columnsResultList, columnsDetailResultList) {
    var ResultList,
      _this = this;

    return ResultList = Backbone.View.extend({
      id: 'resultList',
      tagName: 'div',
      events: {
        'click input': 'changeSelected',
        'click tr': 'triggerInputClick',
        'click td.zoom': 'toggleRow',
        'click td.video a': 'playVideo',
        'click a.back': 'backToGroups'
      },
      options: {
        testGroups: null,
        columns: columnsResultList,
        columnsDetail: columnsDetailResultList
      },
      render: function() {
        var data, table;

        data = this.options.testGroups.toJSON();
        data = data.filter(function(row) {
          return row.count > 0;
        });
        table = $(resultListTmpl({
          columns: this.options.columns,
          data: data
        }));
        this.$el.html(table);
        this.enhanceTable(table, [[10, 'asc'], [9, 'asc'], [11, 'asc']]);
        return this;
      },
      enhanceTable: _.debounce(function(table, sorting) {
        var height;

        if (sorting == null) {
          sorting = [];
        }
        height = table.find('table').parent().height() - 50;
        table.find('table').dataTable({
          'sScrollY': "" + height + "px",
          'bPaginate': false,
          'bScrollCollapse': true,
          'bSortCellsTop': true
        });
        return table.find('th').tipTip({
          defaultPosition: 'left'
        });
      }, 50),
      initialize: function() {
        this.listenTo(this.options.testGroups, 'change:enabled', this.enableChanged);
        this.listenTo(this.options.testGroups, 'change:count', this.refreshTable);
        return this.setSelectionMode(this.options.selectionMode);
      },
      refreshTable: function() {
        return this.render();
      },
      enableChanged: function(model, enabled) {
        var id;

        id = model.get('id');
        return this.$('#' + id).toggleClass('disabled', !enabled);
      },
      changeSelected: function(e) {
        var checkbox, checked, id, model, row;

        checkbox = $(e.currentTarget);
        checked = checkbox.is(':checked');
        row = checkbox.closest('.row');
        id = row.attr('id');
        model = this.options.testGroups.get(id);
        model.set('selected', checked);
        if (this.options.selectionMode === 'exclusive' && checked) {
          return this.unselectAllGroups({
            except: model
          });
        }
      },
      setSelectionMode: function(mode) {
        var changed;

        if (mode !== 'exclusive' && mode !== 'promiscuous') {
          mode = 'promiscuous';
        }
        changed = mode !== this.options.selectionMode;
        this.options.selectionMode = mode;
        if (!changed) {
          return;
        }
        if (mode === 'promiscuous') {
          return this.selectAllGroups();
        } else {
          this.unselectAllGroups();
          return this.selectFirstGroup();
        }
      },
      selectAllGroups: function() {
        this.options.testGroups.each(function(testGroup) {
          return testGroup.set('selected', true);
        });
        return this.updateCheckboxes();
      },
      unselectAllGroups: function(options) {
        this.options.testGroups.each(function(testGroup) {
          if ((options != null ? options.except : void 0) === testGroup) {
            return;
          }
          return testGroup.set('selected', false);
        });
        return this.updateCheckboxes();
      },
      selectFirstGroup: function() {
        var _this = this;

        return _.defer(function() {
          var group, id;

          console.log('select first', _this.options.testGroups.at(0));
          group = _this.options.testGroups.at(0);
          group.set('selected', true);
          id = group.get('id');
          console.log('id', id);
          return _this.$el.find('#' + id + ' input:first').prop('checked', true);
        });
      },
      updateCheckboxes: function() {
        var rows,
          _this = this;

        rows = this.$('.row');
        return rows.each(function(i, row) {
          var $row, chkbox, id, model;

          $row = $(row);
          id = $row.attr('id');
          model = _this.options.testGroups.get(id);
          chkbox = $row.find('input:first');
          return chkbox.prop('checked', model.get('selected'));
        });
      },
      triggerInputClick: function(e) {
        var target;

        target = $(e.target);
        if (target.is('input')) {
          return;
        }
        return target.parent().find('input').trigger('click');
      },
      toggleRow: function(e) {
        var icon, id, row, testGroup;

        e.preventDefault();
        e.stopImmediatePropagation();
        icon = $(e.currentTarget).find('.icon');
        row = $(e.currentTarget).closest('.row');
        id = row.attr('id');
        icon.toggleClass('expanded contracted');
        testGroup = this.options.testGroups.get(id);
        return this.expandTestGroup(testGroup);
      },
      expandTestGroup: function(testGroup) {
        var detailTable, row;

        row = this.$('#' + testGroup.id);
        this.$el.children().hide();
        detailTable = $(resultDetailListTmpl({
          title: testGroup.get('title'),
          columns: this.options.columnsDetail,
          columnsDetail: this.options.columnsDetail,
          detail: testGroup.toJSON(),
          data: testGroup.get('tests').toJSON()
        }));
        this.enhanceTable(detailTable, [[0, 'asc']]);
        return this.$el.prepend(detailTable);
      },
      playVideo: function(e) {
        var a, src;

        a = $(e.currentTarget);
        src = a.attr('href');
        e.preventDefault();
        return this.options.videoPlayback.play(src);
      },
      backToGroups: function(e) {
        this.$('.details').remove();
        return this.$el.children().show();
      }
    });
  });

}).call(this);
