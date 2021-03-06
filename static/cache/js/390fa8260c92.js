window.log=function(){log.history=log.history||[];log.history.push(arguments);if(this.console){arguments.callee=arguments.callee.caller;var newarr=[].slice.call(arguments);(typeof console.log==='object'?log.apply.call(console.log,console,newarr):console.log.apply(console,newarr));}};(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());(function($){$.fn.slugify=function(obj){$(this).data('obj',jQuery(obj));$(this).keyup(function(){var obj=jQuery(this).data('obj');var slug=jQuery(this).val().replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();obj.val(slug);});}})(jQuery)
$(function(){$(".confirm").click(function(){var base=$(this)
var modal=$("#confirm-modal").modal({'backdrop':true,show:true});$("#confirm-modal .message-text").html(base.attr("title"))
$("#confirm-modal .cancel").click(function(){modal.modal('hide');return false;})
$("#confirm-modal .okey").click(function(){window.location.href=base.attr("href");return false})
return false;})})
$(function(){$("#id_start_date, #id_end_date").datepicker({"dateFormat":'yy-mm-dd 00:00:00'});$("#id_title").slugify("#id_slot");})!function($){"use strict"
$.fn.dropdown=function(selector){return this.each(function(){$(this).delegate(selector||d,'click',function(e){var li=$(this).parent('li'),isActive=li.hasClass('open')
clearMenus()!isActive&&li.toggleClass('open')
return false})})}
var d='a.menu, .dropdown-toggle'
function clearMenus(){$(d).parent('li').removeClass('open')}
$(function(){$('html').bind("click",clearMenus)
$('body').dropdown('[data-dropdown] a.menu, [data-dropdown] .dropdown-toggle')})}(window.jQuery||window.ender);!function($){"use strict"
var transitionEnd
$(document).ready(function(){$.support.transition=(function(){var thisBody=document.body||document.documentElement,thisStyle=thisBody.style,support=thisStyle.transition!==undefined||thisStyle.WebkitTransition!==undefined||thisStyle.MozTransition!==undefined||thisStyle.MsTransition!==undefined||thisStyle.OTransition!==undefined
return support})()
if($.support.transition){transitionEnd="TransitionEnd"
if($.browser.webkit){transitionEnd="webkitTransitionEnd"}else if($.browser.mozilla){transitionEnd="transitionend"}else if($.browser.opera){transitionEnd="oTransitionEnd"}}})
var Modal=function(content,options){this.settings=$.extend({},$.fn.modal.defaults,options)
this.$element=$(content).delegate('.close','click.modal',$.proxy(this.hide,this))
if(this.settings.show){this.show()}
return this}
Modal.prototype={toggle:function(){return this[!this.isShown?'show':'hide']()},show:function(){var that=this
this.isShown=true
this.$element.trigger('show')
escape.call(this)
backdrop.call(this,function(){var transition=$.support.transition&&that.$element.hasClass('fade')
that.$element.appendTo(document.body).show()
if(transition){that.$element[0].offsetWidth}
that.$element.addClass('in')
transition?that.$element.one(transitionEnd,function(){that.$element.trigger('shown')}):that.$element.trigger('shown')})
return this},hide:function(e){e&&e.preventDefault()
if(!this.isShown){return this}
var that=this
this.isShown=false
escape.call(this)
this.$element.trigger('hide').removeClass('in')
$.support.transition&&this.$element.hasClass('fade')?hideWithTransition.call(this):hideModal.call(this)
return this}}
function hideWithTransition(){var that=this,timeout=setTimeout(function(){that.$element.unbind(transitionEnd)
hideModal.call(that)},500)
this.$element.one(transitionEnd,function(){clearTimeout(timeout)
hideModal.call(that)})}
function hideModal(that){this.$element.hide().trigger('hidden')
backdrop.call(this)}
function backdrop(callback){var that=this,animate=this.$element.hasClass('fade')?'fade':''
if(this.isShown&&this.settings.backdrop){var doAnimate=$.support.transition&&animate
this.$backdrop=$('<div class="modal-backdrop '+animate+'" />').appendTo(document.body)
if(this.settings.backdrop!='static'){this.$backdrop.click($.proxy(this.hide,this))}
if(doAnimate){this.$backdrop[0].offsetWidth}
this.$backdrop.addClass('in')
doAnimate?this.$backdrop.one(transitionEnd,callback):callback()}else if(!this.isShown&&this.$backdrop){this.$backdrop.removeClass('in')
$.support.transition&&this.$element.hasClass('fade')?this.$backdrop.one(transitionEnd,$.proxy(removeBackdrop,this)):removeBackdrop.call(this)}else if(callback){callback()}}
function removeBackdrop(){this.$backdrop.remove()
this.$backdrop=null}
function escape(){var that=this
if(this.isShown&&this.settings.keyboard){$(document).bind('keyup.modal',function(e){if(e.which==27){that.hide()}})}else if(!this.isShown){$(document).unbind('keyup.modal')}}
$.fn.modal=function(options){var modal=this.data('modal')
if(!modal){if(typeof options=='string'){options={show:/show|toggle/.test(options)}}
return this.each(function(){$(this).data('modal',new Modal(this,options))})}
if(options===true){return modal}
if(typeof options=='string'){modal[options]()}else if(modal){modal.toggle()}
return this}
$.fn.modal.Modal=Modal
$.fn.modal.defaults={backdrop:false,keyboard:false,show:false}
$(document).ready(function(){$('body').delegate('[data-controls-modal]','click',function(e){e.preventDefault()
var $this=$(this).data('show',true)
$('#'+$this.attr('data-controls-modal')).modal($this.data())})})}(window.jQuery||window.ender);!function($){"use strict"
function activate(element,container){container.find('> .active').removeClass('active').find('> .dropdown-menu > .active').removeClass('active')
element.addClass('active')
if(element.parent('.dropdown-menu')){element.closest('li.dropdown').addClass('active')}}
function tab(e){var $this=$(this),$ul=$this.closest('ul:not(.dropdown-menu)'),href=$this.attr('href'),previous,$href
if(/^#\w+/.test(href)){e.preventDefault()
if($this.parent('li').hasClass('active')){return}
previous=$ul.find('.active a').last()[0]
$href=$(href)
activate($this.parent('li'),$ul)
activate($href,$href.parent())
$this.trigger({type:'change',relatedTarget:previous})}}
$.fn.tabs=$.fn.pills=function(selector){return this.each(function(){$(this).delegate(selector||'.tabs li > a, .pills > li > a','click',tab)})}
$(document).ready(function(){$('body').tabs('ul[data-tabs] li > a, ul[data-pills] > li > a')})}(window.jQuery||window.ender);