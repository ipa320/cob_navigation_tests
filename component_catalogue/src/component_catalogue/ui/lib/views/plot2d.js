// Generated by CoffeeScript 1.6.2
(function() {
  define(['backbone'], function(Backbone) {
    return Backbone.View.extend({
      tagName: 'div',
      className: 'plot2d',
      initialize: function() {
        this.colors = ['red', 'green'];
        return this.padding = {
          x: 100,
          y: 100
        };
      },
      drawCircleWithOrientationInRad: function(x, y, phi, color) {
        return this.drawCircleWithOrientationInDeg(x, y, phi / 2.0 / Math.PI * 360, color);
      },
      drawCircleWithOrientationInDeg: function(x, y, phi, color) {
        this.drawArrow(x, y, phi);
        return this.drawCircle(x, y, color);
      },
      drawCircle: function(x, y, color) {
        var circle, radius;

        radius = 3.5;
        circle = this.paper.circle(x, y + .5, radius);
        return circle.attr({
          fill: color,
          stroke: 'transparent'
        });
      },
      drawStartPoint: function(points) {
        var c, nx, ny, startPoint;

        startPoint = points[_.keys(points)[0]][0];
        nx = this.normalizedX(startPoint[1]);
        ny = this.normalizedY(startPoint[2]);
        c = this.paper.circle(nx, ny, 10);
        return c.attr({
          fill: 'orange',
          'stroke-width': 0
        });
      },
      drawArrow: function(x, y, phi) {
        var head, length, line, pathString;

        length = 15;
        pathString = "M0,.5L" + length + ",.5";
        line = this.paper.path(pathString);
        head = this.drawArrowHead();
        line.transform("t" + x + "," + y + "r" + phi + ",0,.5");
        return head.transform("t" + (x + length) + "," + y + "r" + phi + ",-" + length + ",.5");
      },
      drawArrowHead: function() {
        var height, path, width, x1, y0, y1;

        height = 4;
        width = 4;
        y0 = -Math.floor(height / 2) - .5;
        y1 = Math.ceil(height / 2) + 1.5;
        x1 = width + .5;
        path = this.paper.path("M.5,.5L.5," + y0 + "L" + x1 + ",.5L.5," + y1 + "L.5,.5");
        path.attr('fill', 'black');
        return path;
      },
      adjustCanvasToPoints: function(points) {
        var rawPoints, x, xMax, xMin, y, yMax, yMin, _ref, _ref1;

        rawPoints = _(points).chain().values().flatten(true).value();
        x = _.map(rawPoints, function(p) {
          return p[1];
        });
        y = _.map(rawPoints, function(p) {
          return p[2];
        });
        _ref = [_.min(x), _.max(x)], xMin = _ref[0], xMax = _ref[1];
        this.mx = (this.width - 2 * this.padding.x) / (xMax - xMin);
        this.cx = this.padding.x - this.mx * xMin;
        _ref1 = [_.min(y), _.max(y)], yMin = _ref1[0], yMax = _ref1[1];
        this.my = (this.height - 2 * this.padding.y) / (yMax - yMin);
        return this.cy = this.padding.y - this.my * yMin;
      },
      normalizedX: function(x) {
        return this.mx * x + this.cx;
      },
      normalizedY: function(y) {
        return this.my * y + this.cy;
      },
      drawLine: function(linePoints, color) {
        var linePath, nx, ny, obj, point, _i, _len;

        linePath = ['M'];
        for (_i = 0, _len = linePoints.length; _i < _len; _i++) {
          point = linePoints[_i];
          nx = Math.round(this.normalizedX(point[1])) + .5;
          ny = Math.round(this.normalizedY(point[2])) + .5;
          linePath.push(nx, ',', ny, 'L');
        }
        linePath.pop();
        obj = this.paper.path(linePath.join(''));
        return obj.attr({
          stroke: color
        });
      },
      renderPoints: function(points) {
        var color, data, i, key, nx, ny, phi, point, x, y, _results;

        if (!points) {
          return;
        }
        if (this.paper) {
          this.paper.remove();
        }
        this.width = this.$el.width();
        this.height = this.$el.height();
        console.log('w/h: ', this.width, this.height);
        this.paper = Raphael(this.$el[0], this.width, this.height);
        this.adjustCanvasToPoints(points);
        i = 0;
        this.drawStartPoint(points);
        _results = [];
        for (key in points) {
          data = points[key];
          color = this.colors[i++];
          this.drawLine(data, color);
          _results.push((function() {
            var _i, _len, _ref, _ref1, _results1;

            _results1 = [];
            for (_i = 0, _len = data.length; _i < _len; _i++) {
              point = data[_i];
              _ref = point.slice(1, 4), x = _ref[0], y = _ref[1], phi = _ref[2];
              _ref1 = [this.normalizedX(x), this.normalizedY(y)], nx = _ref1[0], ny = _ref1[1];
              _results1.push(this.drawCircleWithOrientationInRad(nx, ny, phi, color));
            }
            return _results1;
          }).call(this));
        }
        return _results;
      },
      render: function() {
        return this;
      }
    });
  });

}).call(this);
