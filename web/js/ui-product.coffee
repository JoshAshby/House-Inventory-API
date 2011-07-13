spam = 0
	
$.ajaxSetup
	cache: false

base = 'http://localhost/'

acorn = base + 'product/'

frand = {
	'picture': ( base + 'picture/')
	'thumb': ( base + 'thumb/')
	'info': '/info/'
	'cat': (base + 'category/')
}

a = (mop) ->
	$.getJSON acorn + mop + frand['info'], (data) ->
		if data
			$('#hamlet_error').hide()
			$('#name').html data['name']
			$('#barcode').html data['barcode']
			$('#quantity').html data['quantity']
			$('#category').html "<a href='category.html?category=#{ data['cat'] }'>#{ data['cat'] }</a>"
			$('#description').html data['description']
			$('#picture').html "<img src='#{ frand['thumb'] + data['picture'] }' alt='#{ data['picture'] }' width='128px'/>"
		else
			$('#hamlet').hide()
	
$ ->
	b = $.getUrlVars()
	if b['barcode']
		a(b['barcode'])
	else
		$("#hamlet").hide()
		$("#error").show()
		
	$('#home').button()