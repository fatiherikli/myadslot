
// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console) {
    arguments.callee = arguments.callee.caller;
    var newarr = [].slice.call(arguments);
    (typeof console.log === 'object' ? log.apply.call(console.log, console, newarr) : console.log.apply(console, newarr));
  }
};

// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());



// http://djangosnippets.org/snippets/1488/
(function ($) {
    $.fn.slugify = function(obj) {
        $(this).data('obj', jQuery(obj));
        $(this).keyup(function() {
            var obj = jQuery(this).data('obj');
            var slug = jQuery(this).val().replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
            obj.val(slug);
        });
    }
})(jQuery)



$(function () {
    $(".confirm").click(function () {
        var base = $(this)
        var modal = $("#confirm-modal").modal({'backdrop':true, show:true});
        $("#confirm-modal .message-text").html(base.attr("title"))
        $("#confirm-modal .cancel").click(function () {modal.modal('hide'); return false;})
        $("#confirm-modal .okey").click(function () { window.location.href = base.attr("href"); return false })
        return false;
    })
})