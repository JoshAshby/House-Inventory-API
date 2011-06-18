(function($) {

	var methods = {
		init : function() {
			return function () {$(this).attr('contenteditable', 'true');
			var old_val;
			old_val = $(this).html();
			
			$(this).hover( function() {
				$(this).addClass("hover");
			}, function () {
				$(this).removeClass("hover");
			});
			
			$(this).focusin( function() {
				$(this).addClass("edit");
			});
			
			$(this).focusout( function (event) {
				$(this).removeClass("edit");
				var new_val;
				new_val = $(this).html();
				if (old_val != new_val) {
					$(this).addClass('changed');
				}
			});
		};
		}, destroy : function( ) {
			return this.each(function(){
				$(this).attr('contenteditable', 'false');
				$(window).unbind('.edit');
			});
		}
	};

	$.fn.edit = function(method) {
		 if ( methods[method] ) {
			return methods[method];
		}
	};
})(jQuery);