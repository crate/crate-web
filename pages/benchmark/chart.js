  var labelName = "method";
  var versionName = "version";
  var xSeries = "timestamp";
  var avgSeries = "avg";
  var stddevSeries = "stddev";
  var showDays = 30;

  var endpoint = '/benchmark/api/';
  var groups = [
    "BulkInsertBenchmark",
    "BulkDeleteBenchmark",
    "InsertBenchmark",
    "CountBenchmark",
    "GroupByBenchmark",
    "GroupByArbitraryBenchmark",
    "CrossJoinBenchmark",
    "AnyBenchmark",
    "LikeBenchmark",
    "InStringBenchmark",
    "InNumericBenchmark",
    "ESScrollingBenchmark",
    "BaseCreateBenchmark",
    "CreateWith10TablesBenchmark",
    "CreateWith200TablesBenchmark",
    "InformationSchemaBenchmark",
    "AddingTableColumnsBenchmark"
  ];

  function fetchData(url) {
    return new Promise(function(succeed, fail) {
      var req = new XMLHttpRequest();
      req.open("GET", url, true);
      req.addEventListener("load", function() {
        if (req.status < 400)
          succeed(JSON.parse(req.responseText));
        else
          fail(new Error("Request failed: " + req.statusText));
      });
      req.addEventListener("error", function() {
        fail(new Error("Network error"));
      });
      req.send(null);
    });
  };

  function transformData(data) {
    var rows = [];
    var labels = [];
    var annotations = [];
    var header = "";
    if (data && data.length > 0) {
      var datatable = {};
      header = data[0]["group"];

      labels = Object.keys(data.reduce(function(d, cur) {
        var lbl = cur[labelName];
        d[lbl] = 0;
        return d;
      }, {}));

      var latestVersion = "";
      data.forEach(function(row) {
        var x = row[xSeries];

        if (!(x in datatable))
          datatable[x] = {};
        datatable[x][row[labelName]] = row[avgSeries];
        if (row[versionName] !== latestVersion) {
          latestVersion = row[versionName];
          var annotation = {
            series: row[labelName],
            x: row[xSeries],
            shortText: row[versionName],
            text: row[versionName],
            width: 50
          };
          annotations.push(annotation);
        }

      });

      rows = Object.keys(datatable).sort().map(function(x) {
        var row = labels.map(function(lbl) {
          if (!(lbl in datatable[x]))
            return null
          else
            return datatable[x][lbl];
        });
        row.unshift(x);
        return row;
      });
    }
    labels.unshift("date");

    return {
      rows: rows,
      labels: labels,
      annotations: annotations,
      header: header
    };
  };

  function draw(drawDiv) {
    function dateFormat(x) {
      var val = new Date(parseInt(x));
      return val.toDateString();
    }
    return function(datatable) {
      var options = {
        labelsDiv: document.getElementById(datatable.header + '_labels'),
        labels: datatable.labels,
        errorBars: false,
        ylabel: 'avg time of a run in seconds',
        digitsAfterDecimal: 4,
        axes: {
          x: {
            valueFormatter: dateFormat,
            axisLabelFormatter: dateFormat
          }
        },
        showRangeSelector: false
      };
      var chart = new Dygraph(drawDiv, datatable.rows, options);
      chart.setAnnotations(datatable.annotations)
    };
  }
  window.onload = function() {
    var now = new Date();
    now.setDate(now.getDate() + 1);
    var past = new Date();
    past.setDate(now.getDate() - 30);
    var start = past.toISOString().split("T")[0];
    var end = now.toISOString().split("T")[0];

    groups.forEach(function(group) {
      var url = endpoint + group + "?from=" + start + "&to=" + end;
      fetchData(url).then(transformData).then(draw(document.getElementById(group)));
    });

  }
