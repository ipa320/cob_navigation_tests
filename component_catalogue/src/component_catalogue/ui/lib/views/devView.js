// Generated by CoffeeScript 1.6.2
(function() {
  define(['backbone', 'templates/devView', 'views/componentDevView', 'views/applicationDevView'], function(Backbone, devViewTmpl, ComponentDevView, ApplicationDevView) {
    return Backbone.View.extend({
      tagName: 'div',
      className: 'developerView',
      events: {
        'click .tab.component': "activateComponentView",
        'click .tab.application': "activateApplicationView"
      },
      render: function() {
        this.$el.html(devViewTmpl());
        this.activateApplicationView();
        return this;
      },
      initialize: function() {
        this.applicationDevView = new ApplicationDevView({
          testGroups: this.options.testGroups,
          sortingOptions: this.options.sortingOptions
        });
        return this.componentDevView = new ComponentDevView({
          testGroups: this.options.testGroups,
          sortingOptions: this.options.sortingOptions
        });
      },
      renderComponentDevView: function($el) {
        $el.html(this.componentDevView.render().el);
        return $('#sortingOptionsContainer').show();
      },
      renderApplicationDevView: function($el) {
        $el.html(this.applicationDevView.render().el);
        return $('#sortingOptionsContainer').hide();
      },
      activateApplicationView: function() {
        if (this.activeTab() !== 'application') {
          this.activateTab('application');
          this.trigger('changeView', 'application');
          return this.renderApplicationDevView(this.$('.tabContent'));
        }
      },
      activateComponentView: function() {
        if (this.activeTab() !== 'component') {
          this.activateTab('component');
          this.trigger('changeView', 'component');
          return this.renderComponentDevView(this.$('.tabContent'));
        }
      },
      activeTab: function() {
        return this.activeTabName;
      },
      activateTab: function(name) {
        this.$('.tab.active').removeClass('active');
        this.$('.tab.' + name).addClass('active');
        return this.activeTabName = name;
      }
    });
  });

}).call(this);
