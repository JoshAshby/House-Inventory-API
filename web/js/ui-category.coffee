spam = 0
	
$.ajaxSetup
	cache: false

base = 'http://localhost/'

acorn = base + 'category/'

frand = {
	'thumb': ( base + 'thumb/')
}

update = (cat) ->
	$.getJSON (acorn + cat + '/'), (data) ->
		if data
			$('#romeo').show()
			$('#romeo_error').hide()
			$('#romeo').html ''
			f = data['products']
			(if i%2 == 0
				b = 'shade'
			else
				b = ''
			$('#romeo').append "<tr class='pro public #{ b }' id='#{ f[i]['barcode'] }'><td><a href='#{ 'product.html?barcode=' + f[i]['barcode'] }'><img src='#{ frand['thumb'] + f[i]['picture'] }' alt='#{ f[i]['picture'] }' width='64px'/></a></td><td><b class='blue'>#{ f[i]['name'] }<b></td><td>#{ f[i]['barcode'] }</td></tr>"
			$('#'+f[i]['barcode']).clicker('init') ) for i in [0..f.length-1]
		else
			$("#romeo").hide()
			$('#romeo_error').show()
		
death = ->
	$.getJSON acorn, (data) ->
		if data
			$('#juliet').show()
			$('#romeo_error').hide()
			$('#juliet').html ''
			d = data['categories']
			(if i%2 == 0
				b = 'shade'
			else
				b = ''
			$('#juliet').append "<tr class='pro public #{ b }' id='#{ d[i] }'><td><a href='#{ 'category.html?category=' + d[i] }'>#{ d[i] }</a></td></tr>"
			$('#'+d[i]).clicker('init') ) for i in [0..d.length-1]
		else
			$("#juliet").hide()
			$('#romeo_error').show()
	
$ ->
	b = $.getUrlVars()
	c = b['category']
	if c
		$("#itally").hide()
		update(c)
		$('#category').html c
	else
		$("#florence").hide()
		$("#itally").show()
		$('#category').html "List"
		death()
	
		
	$('#home').button()