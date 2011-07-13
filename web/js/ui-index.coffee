spam = 0
	
$.ajaxSetup
	cache: false

base = 'http://localhost/'
	
acorn = base + 'product/'
	
frand = {
	'picture': ( base + 'picture/')
	'thumb': ( base + 'thumb/')
	'info': '/info/'
	'category': '/category/'
}

update = ->
	$.getJSON acorn, (data) ->
		if data
			$('#peanut').show()
			$('#peanut_error').hide()
			$('#peanut').html ''
			(if i%2 == 0
				b = 'shade'
			else
				b = ''
			$('#peanut').append "<tr class='pro public #{ b }' id='#{ data[i]['barcode'] }'><td><a href='#{ 'product.html?barcode=' + data[i]['barcode'] }'><img src='#{ frand['thumb'] + data[i]['picture'] }' alt='#{ data[i]['picture'] }' width='64px'/></a></td><td><b class='blue'>#{ data[i]['name'] }<b></td><td>#{ data[i]['barcode'] }</td><td>#{ data[i]['flag'] }</td></tr>"
			$('#'+data[i]['barcode']).clicker('init')) for i in [0..data.length-1]
		else
			$("#peanut").hide()
			$('#peanut_error').show()
			
$ ->
	update()
	