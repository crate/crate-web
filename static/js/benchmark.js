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
  // for local develpment uncomment next line
  // endpoint = 'http://localhost:8080/result';

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
    return releases.map(function(e) {
      e['series'] = options.labels[1];
      return e;
    });
  };

  function dateFormat(x) {
    var val = new Date(parseInt(x));
    return val.toDateString();
  };

  function setLabels(datatable){
    switch (datatable.header){
      case 'single_ops':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('delete') !== -1 ){
            $('#'+datatable.header + '_single_delete').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Single Delete: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Single Delete';

          }
          if(datatable.labels[i].indexOf('insert') !== -1 ){
            $('#'+datatable.header + '_single_insert').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Single INSERT: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Single Insert';

          }
          if(datatable.labels[i].indexOf('update') !== -1 ){
            $('#'+datatable.header + '_single_update').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Single UPDATE: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Single Update';
          }

        }
        break;

      case 'bulk_ops':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('delete') !== -1 ){
            $('#'+datatable.header + '_delete').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Bulk Delete: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Bulk Delete';

          }
          if(datatable.labels[i].indexOf('insert') !== -1 ){
            $('#'+datatable.header + '_insert').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Bulk INSERT: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Bulk Insert';

          }
          if(datatable.labels[i].indexOf('update') !== -1 ){
            $('#'+datatable.header + '_update').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Bulk UPDATE: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Bulk Update';
          }

        }
        break;

      case 'in_numeric':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('date') === -1 ){
            $('#'+datatable.header + '_numeric').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> In Numeric: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'In Numeric';
          }
          
        }
        break;   

      case 'in_string':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('date') === -1 ){
            $('#'+datatable.header + '_string').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> In String: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'In String';
          }
          
        }
        break;   

      case 'array':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('!= any') !== -1 ){
            $('#'+datatable.header + '_not_any').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> != ANY(): </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = '!= ANY()';
          }
          if(datatable.labels[i].indexOf('= any') !== -1 ){
            $('#'+datatable.header + '_any').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> = ANY(): </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = '= ANY()';
          }
          
        }
        break;   

      case 'aggregations':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('count("cCode")') !== -1 ){
            $('#'+datatable.header + '_count_col').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">count(columnName): </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'count(columnName)';
          }
          if(datatable.labels[i].indexOf('select count(*) from uservisits') !== -1 ){
            $('#'+datatable.header + '_count_all').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">count(*): </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'count(*)';
          }

          if(datatable.labels[i].indexOf('select "cCode", count(*) from uservisits group by "cCode"') !== -1 ){
            $('#'+datatable.header + '_count_all_grp_by').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">count(*) group by: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'count(*) group by';
          }

          if(datatable.labels[i].indexOf('arbitrary') !== -1 ){
            $('#'+datatable.header + '_arbitrary').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">arbitrary: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'arbitrary';
          }

          if(datatable.labels[i].indexOf('avg') !== -1 ){
            $('#'+datatable.header + '_avg').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">avg: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'avg';
          }

          if(datatable.labels[i].indexOf('distinct') !== -1 ){
            $('#'+datatable.header + '_count_distinct').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">count distinct: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'count distinct';
          }

          if(datatable.labels[i].indexOf('max') !== -1 ){
            $('#'+datatable.header + '_max').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">max: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'max';
          }
          
          if(datatable.labels[i].indexOf('min') !== -1 ){
            $('#'+datatable.header + '_min').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;">min: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'min';
          }
          
        }
        break;  

      case 'partitions':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('insert') !== -1 ){
            $('#'+datatable.header + '_insert').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Insert: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Insert';

          }
          if(datatable.labels[i].indexOf('select') !== -1 ){
            $('#'+datatable.header + '_select').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Select: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Select';

          }
          if(datatable.labels[i].indexOf('update') !== -1 ){
            $('#'+datatable.header + '_update').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> UPDATE: </span>' + '<span >' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Update';
          }

        }
        break;

      case 'system':
        for (i=0; i < datatable.labels.length; i++){
          if(datatable.labels[i].indexOf('date') === -1 ){
            $('#'+datatable.header + '_select').html('<span style="color:'+colorSchema[i-1]+'; font-weight:600;"> Select: </span> ' + '<span>' + datatable.labels[i] + '</span>');
            datatable.labels[i] = 'Select';
          }
          
        }
        break;           
    }

  };

  function draw(drawDiv) {
    return function(datatable) {
      setLabels(datatable);
      var options = {
        labelsDiv: document.getElementById(datatable.header + '_labels'),
        labels: datatable.labels,
        hideOverlayOnMouseOut: false,
        labelsSeparateLines: true,
        colors: colorSchema,
        errorBars: false,
        ylabel: 'avg time of single iteration in seconds',
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
