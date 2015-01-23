;(function($){

  /**
   * Crate.IO main.js
   */

  var ga = window.ga || function(){ console.warn('GA not enabled'); };

  var EMAIL_RE = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

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
    var email = this.email.value;
    var uid = $.cookie('uid');
    e.preventDefault();

    var group = $('.form-group-email', this);
    group.removeClass('has-error');

    if (email.length > 0 && uid) {
      var valid = EMAIL_RE.test(email);
      if (!valid) {
        group.addClass('has-error');
        $('.text-danger', group).removeClass('hide');
        return;
      }

      var guid = new Date().getTime() + uid;
      analytics.identify(uid, {
        'email': email
      }, {
        'integrations': {
          'All': false,
          'Intercom': true
        }
      });
      analytics.track('Signed up for download', {
        'event_guid': guid,
        'user_email': email
      });
    }
    ga('send', 'event', 'button', 'click', 'download_download', 1);
    window.open(url, '_blank');
    this.reset();
  });

}(jQuery));
