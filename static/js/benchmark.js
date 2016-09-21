(function() {

  var labelName = "statement";
  var versionName = "build_version";
  var xSeries = "build_timestamp";
  var avgSeries = "median";
  var stddevSeries = "stdev";
  var showDays = 30;
  var releases = [];
  var headerPosition = $('.cr-nav').position().top;

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
  if (['localhost', '127.0.0.1'].indexOf(window.location.hostname) > -1) {
    // for local develpment we assume the benchmark api is running on localhost:8080
    endpoint = 'http://localhost:8080/result';
  };

  function transformData(data) {
    var rows = [];
    var labels = [];
    var header = "";
    if (data && data.length > 0) {
      var datatable = {};
      header = data[0]["benchmark_group"];

      labels = Object.keys(data.reduce(function(d, cur) {
        var lbl = cur[labelName];
        d[lbl] = 0;
        return d;
      }, {}));

      data.forEach(function(row) {
        var x = row[xSeries];
        if (!(x in datatable)) datatable[x] = {};
        datatable[x][row[labelName]] = [row[avgSeries], row[stddevSeries]];
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
    return releases.map(function(e) {
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
        ylabel: 'avg time of single iteration in seconds',
	interactionModel: Dygraph.Interaction.nonInteractiveModel_,
	errorBars: true,
        axes: {
          x: {
            valueFormatter: dateFormat,
            axisLabelFormatter: dateFormat,
            drawGrid: false
          },
          y: {
            valueRange: [0, null],
            drawGrid: false
          }
        },
        showRangeSelector: false,
        highlightSeriesOpts: {
          strokeWidth: 3,
          strokeBorderWidth: 1,
          highlightCircleSize: 5
        }
      };
      var chart = new Dygraph(drawDiv, datatable.rows, options);
      chart.setAnnotations(createAnnotations(options, releases));
    };
  };

  // fix navigation header to top after scroll 
  $(window).scroll(function() {

    var scrollPosition = $(this).scrollTop();
    var margin = 150;

    // set header to sticky
    if (scrollPosition > headerPosition) {
      $('.cr-nav').addClass("sticky");
    } else {
      $('.cr-nav').removeClass("sticky");
    }

    // set cr-nav-item to active when window scrolls
    $('.cr-nav .cr-nav-item').each(function() {
      var refElement = $(this).attr('scroll-to-chart');
      if ($('#' + refElement + '_tab').position().top - margin <= scrollPosition && $('#' + refElement + '_tab').position().top + $('#' + refElement + '_tab').height() > scrollPosition + margin) {

        $(this).addClass("cr-nav-item--active");
      } else {
        $(this).removeClass("cr-nav-item--active");
      }
    });

  });

  $(document).ready(function(e) {
    var now = new Date();
    now.setDate(now.getDate() + 1);
    var past = new Date();
    past.setDate(now.getDate() - showDays);
    var start = past.toISOString().split("T")[0];
    var end = now.toISOString().split("T")[0];

    $(".chart").each(function(idx, elem) {
      var url = endpoint + "/" + elem.id + "?from=" + start + "&to=" + end;
      $.get(url).then(transformData).then(draw(elem));
    });
  });

  // on click scroll to corresponding graph 
  $(".cr-nav-item").click(
    function() {
      var chart_id = $(this).attr('scroll-to-chart');
      var margin = 50;

      //scroll to chart
      $('body').scrollTop($('#' + chart_id + '_tab').position().top - $('.cr-nav').height() - margin);

      // set cr-nav-item item to active
      if (!$(this).hasClass("cr-nav-item--active")) {
        $(".cr-nav-item").removeClass("cr-nav-item--active");
        $(this).addClass("cr-nav-item--active");
      }
    }
  );

})();
