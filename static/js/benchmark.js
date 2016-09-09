(function() {

  var labelName = "method";
  var versionName = "version";
  var xSeries = "build_timestamp";
  var avgSeries = "avg";
  var stddevSeries = "stddev";
  var showDays = 30;
  var releases = [];
  /**
   * Example annotation of a release:
   *
    {
      shortText: '0.54.0',
      text: 'Released on 2015/12/16',
      x: 1453860104000,
      width: 50,
      clickHandler: function(e) {
        window.open('https://github.com/crate/crate/blob/0.54.0/CHANGES.txt#L8');
      }
    }
  **/
  var colorSchema = [
    "#0074D9",
    "#001F3F",
    "#85144b",
    "#F012BE",
    "#FF4136",
    "#FF851B",
    "#FFDC00",
    "#2ECC40",
    "#3D9970",
    "#AAAAAA"
  ];

  var endpoint = '/benchmark/api';
  // for local develpment uncomment next line
  // endpoint = 'http://localhost:8080/result';
  var groups = [
    "insert",
    "update",
    "delete",
    "sequence",
    "array",
    "aggregations",
    "joins",
    "partitions",
    "system"
  ];

  function transformData(data) {
    var rows = [];
    var labels = [];
    var header = "";
    if (data && data.length > 0) {
      var datatable = {};
      header = data[0]["group"];

      labels = Object.keys(data.reduce(function(d, cur) {
        var lbl = cur[labelName];
        d[lbl] = 0;
        return d;
      }, {}));

      data.forEach(function(row) {
        var x = row[xSeries];
        if (!(x in datatable)) datatable[x] = {};
        datatable[x][row[labelName]] = row[avgSeries];
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
      header: header
    };
  };

  function createAnnotations(options, releases) {
    return releases.map(function(e){
      e['series'] = options.labels[1];
      return e;
    });
  };

  function dateFormat(x) {
    var val = new Date(parseInt(x));
    return val.toDateString();
  };

  function draw(drawDiv) {
    return function(datatable) {
      var options = {
        labelsDiv: document.getElementById(datatable.header + '_labels'),
        labels: datatable.labels,
        colors: colorSchema,
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
      chart.setAnnotations(createAnnotations(options, releases));
    };
  };

  $(document).ready(function(e) {
    var now = new Date();
    now.setDate(now.getDate() + 1);
    var past = new Date();
    past.setDate(now.getDate() - showDays);
    var start = past.toISOString().split("T")[0];
    var end = now.toISOString().split("T")[0];

    groups.forEach(function(group) {
      var url = endpoint + "/" + group + "?from=" + start + "&to=" + end;
      $.get(url).then(transformData).then(draw(document.getElementById(group)));
    });
  });

})();
