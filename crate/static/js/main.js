;(function($){

  /**
  * Crate.IO main.js
  */

  var ga = window.ga || function(){ console.warn('GA not enabled'); };

  /**
  * Email input field on download page
  */
  $('input.form-control').on('focus', function(e){
    var control = $(this).parent().parent();
    control.removeClass('has-error');
    $('.text-danger', control).addClass('hide');
  });

  $('form.crate-cli').each(function(idx, elem){
    var term = new Term(elem);
    term.addComment('# Why not start with the following query?');
    term.addComment('# SELECT id, name, hostname FROM sys.nodes;');
    term.addComment('# Execute the examples on the right by clicking into the code box.');
    window.term = term;
  });

  $('pre.tut').each(function(idx, elem) {
    var tname = 'table_' + ($.cookie('uid') || 'foo');
    $(elem).text(elem.textContent.replace('T_NAME', tname));
    hljs.highlightBlock(elem);
    $(elem).tooltip({'title':'Click to execute query!', 'placement':'top'});
  });

  $('pre.tut').on('click', function(e){
    window.term.exec(this.textContent);
  });


  $('form#form-download').on('submit', function(e){
    var url = $(this).data('url');
    e.preventDefault();


    if (url) {
      ga('send', 'event', 'button', 'click', 'download_download', 1);
      window.open(url, '_blank');
      this.reset();
    }
  });

}(jQuery));
