$(function() {
  $.widget("custom.dynachart", {
    options : {
      configUrl : "/api/v1/chart/config",
      dataUrl : "/api/v1/chart/data",
      divId : "requiresUniqueId",
      autoPlay : true
    },
    _create : function() {
      var self = this;

      this.day = 0;
      this.firstDate = new Date();

      this.chartDiv = $("<div>", {
        "id" : this.options.divId,
        "style" : "width: 100%; height: 400px;"
      });
      this.element.append(this.chartDiv);
      this._createOptions();

      this.chartData = [];
      this.graphs = [];

      // LOAD GRAPH CONFIG
      $.ajax({
        url : this.options.configUrl,
        type : "GET",
        dataType : "json",
        success : function(data) {
          console.log("ajax", data);
          for ( var i in data.graphs) {
            console.log(data.graphs[i]);
            self.graphs.push({
              title : data.graphs[i].title,
              id : data.graphs[i].id,
              valueAxis : "v1",
              valueField : data.graphs[i].valueField,
              bullet : "round",
              bulletBorderColor : "#FFFFFF",
              bulletBorderAlpha : 1,
              lineThickness : 2,
              lineColor : data.graphs[i].lineColor,
              negativeLineColor : "#0352b5",
              balloonText : "[[category]]<br><b><span style='font-size:14px;'>"+data.graphs[i].title+": [[value]]</span></b>"
            });

          } // for
          console.log(self.graphs);
          self._createAfterGraphLoad();
        }
      });
    },
    _createAfterGraphLoad : function() {
      this._createChart();

      if (this.options.autoPlay) {
        this._playChart();
      }
    },
    _createChart : function() {
      var self = this;
      this.chart = AmCharts.makeChart(this.options.divId, {
        type : "serial",
        pathToImages : "../amcharts/images/",
        dataProvider : this.chartData,
        categoryField : "ts",
        categoryAxis : {
          categoryFunction : function(value) {
            return new Date(value * 1000);
          },
          parseDates : true,
          gridAlpha : 0.15,
          minorGridEnabled : true,
          axisColor : "#DADADA",
          minPeriod : "ss"
        },
        valueAxes : [ {
          axisAlpha : 0.2,
          id : "v1"
        } ],
        graphs : this.graphs,
        chartCursor : {
          fullWidth : true,
          cursorAlpha : 0.1
        },
        chartScrollbar : {
          scrollbarHeight : 40,
          color : "#FFFFFF",
          autoGridCount : true,
          graph : "g1"
        }
      });
    },
    _createOptions : function() {
      var self = this;
      var fnSelect = function() {
        self.setMode("select");
      };
      var fnPan = function() {
        self.setMode("pan");
      };
      var fnLive = function() {
        self.setMode("live")
      }

      var mkButton = function(label, icon, fnClick) {
        var button = $("<button>", {
          "type" : "button",
          "class" : "btn btn-default"
        }).click(fnClick);
        button.append($("<span>", {
          "class" : "glyphicon glyphicon-" + icon,
          "style" : "margin-right:5px"
        }))
        button.append($("<span>").text(label));
        return button;
      }

      this.optionsToolbar = $("<div>", {
        "class" : "btn-toolbar",
        "role" : "toolbar",
        "style" : "margin-left:32px"
      })
      this.optionsGroup = $("<div>", {
        "class" : "btn-group"
      });
      this.optionSelect = mkButton("Select", "resize-horizontal", fnSelect);
      this.optionPan = mkButton("Pan", "hand-up", fnPan);
      this.optionLive = mkButton("Live", "refresh", fnLive);

      this.optionsGroup.append(this.optionSelect);
      this.optionsGroup.append(this.optionPan);
      this.optionsGroup.append(this.optionLive);
      this.optionsToolbar.append(this.optionsGroup);
      this.element.append(this.optionsToolbar);
    },
    _playChart : function() {
      var self = this;
      self.playing = true;

      self.interval = setInterval(function() {
        // remove datapoint from the beginning
        // self.chart.dataProvider.shift();
        // LOAD GRAPH CONFIG
        $.ajax({
          url : self.options.dataUrl,
          type : "GET",
          dataType : "json",
          success : function(data) {
            console.log(data);
            self.chart.dataProvider.push(data);
            self.chart.validateData();
            self.zoomChart();
          }
        });
      }, 1000);
    },
    zoomChart : function() {
      // different zoom methods can be used - zoomToIndexes, zoomToDates,
      // zoomToCategoryValues
      this.chart.zoomToIndexes(this.chartData.length - 40, this.chartData.length - 1);
    },
    setMode : function(mode) {
      var chartCursor = this.chart.chartCursor;

      if (mode == "select") {
        chartCursor.pan = false;
        chartCursor.zoomable = true;
        clearInterval(this.interval);
        this.playing = false;
      } else if (mode == "pan") {
        chartCursor.pan = true;
        chartCursor.zoomable = false;
        clearInterval(this.interval);
        this.playing = false;
      } else if (mode == "live") {
        if (this.playing == false) {
          chartCursor.pan = false;
          chartCursor.zoomable = false;
          this._playChart();
        }
      }
      console.log("MODE!", mode);

    }
  }); // $.widget
});// $()
