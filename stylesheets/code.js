
/* the next line is an example of how you can override default options globally (currently commented out) ... */

  // $.fn.cluetip.defaults.tracking = true;
  // $.fn.cluetip.defaults.width = 'auto';
  // $.fn.cluetip.defaults.sticky = true;
  // $.fn.cluetip.defaults.arrows = true;

$(document).ready(function() {

 // $.cluetip.setup({insertionType: 'insertBefore', insertionElement: 'div:first'});
 // $.fn.cluetip.defaults.ajaxSettings.beforeSend = function(ct) {
 //     console.log(this);
 // };

//default theme
  $('a.title').cluetip({splitTitle: '|'});
  });
  