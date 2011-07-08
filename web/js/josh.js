(function($) {

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
				}
			});
		} else if (method === 'destroy') {
			$(this).attr('contenteditable', 'false');
			$(this).unbind('mouseover.edit');
			$(this).unbind('mouseout.edit');
			$(this).unbind('focusin.edit');
			$(this).unbind('focusout.edit');
			if ($(this).hasClass('changed')) {
				$(this).removeClass('changed');
			}
		}
	};
})(jQuery);