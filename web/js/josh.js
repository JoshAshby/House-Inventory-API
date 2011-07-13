(function($) {
	$.fn.clicker = function(method, area) {
		if (method ==='init') {
			oldbg = $(this).css('background');
			$(this).bind('mousedown.clicker', function() {
				$(this).css('background', '#B2BEB5');
				window.location = $(this).find('a').attr('href');
			});
			$(this).bind('mouseup.clicker', function() {
				$(this).css('background', oldbg);
			});
			$(this).bind('mouseover.clicker', function() {
				$(this).css('background', '#F0EAD6');
			});
			$(this).bind('mouseout.clicker',  function () {
				$(this).css('background', oldbg);
			});
		};
	};

	$.fn.edit = function(method) {
		if (method ==='init') {
			$(this).attr('contenteditable', 'true');
			var old_val;
			old_val = $(this).html();
			
			$(this).bind('mouseover.edit', function() {
				$(this).addClass("hover");
			});
			$(this).bind('mouseout.edit',  function () {
				$(this).removeClass("hover");
			});
			
			$(this).bind('focusin.edit', function() {
				$(this).addClass("edit");
			});
			$(this).bind('focusout.edit', function (event) {
				$(this).removeClass("edit");
				var new_val;
				new_val = $(this).html();
				if (old_val != new_val) {
					$(this).addClass('changed');
				};
			});
		} else if (method === 'destroy') {
			$(this).attr('contenteditable', 'false');
			$(this).unbind('mouseover.edit');
			$(this).unbind('mouseout.edit');
			$(this).unbind('focusin.edit');
			$(this).unbind('focusout.edit');
			if ($(this).hasClass('changed')) {
				$(this).removeClass('changed');
			};
		};
	};
})(jQuery);

$.extend({
	getUrlVars: function() {
		var vars = [], hash;
		var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		for (var i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
		},
		getUrlVar: function(name){
		return $.getUrlVars()[name];
	}
});

$('#sidebar').load('sidebar.html');
