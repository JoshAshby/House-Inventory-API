package database;
use warnings;
use strict;
use DBI;
use DBD::mysql;
use JSON;
use Statistics::LineFit;
use DateTime;
use DateTime::Format::MySQL;

#For printing out the JSON formated strings
my $json = new JSON;
 
#This is for all the database related info, to make sure no one can easily see it.
do 'db_info.pl';

#Prototypes for database functions
our $get_all_products;
our $get_product_db;
our $add_new_product;
our $update_quantity;
our $remove_product;
our $get_stats;
our $update_product_db;

#Setting up a new API call
sub new {
	my $class = shift;
	my $self = {};

	bless ($self, $class);
	return $self;
}

#print the info for just one product
sub print_info {
	my $query = @_[1];
	my $name;
	my $description;
	my $barcode;
	my $quantity;
	my $flag;
	my $average_days_left;
	$get_product_db->execute($query,$query);
	$get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
	my $p_text;
	while($get_product_db->fetch()){
		my %text = ('name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
		$p_text = $json->encode(\%text);
	}
	return $p_text;
}

sub return_info {
	my $query = @_[1];
	my $name;
	my $description;
	my $barcode;
	my $quantity;
	my $flag;
	my $average_days_left;
	$get_product_db->execute($query,$query);
	$get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
	my $p_text;
	while($get_product_db->fetch()){
		my %text = ('name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
		return %text;
	}
}

#print the total inventory for the database
sub total_inventory {
	my $name;
	my $description;
	my $barcode;
	my $quantity;
	my $flag;
	$get_all_products->execute();
	$get_all_products->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag);
	my @data_hash;
	while($get_all_products->fetch()){
		my %otext = ('name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag);
		push(@data_hash, \%otext);
	}
	return $json->encode(\@data_hash);
}

#update one products info
sub update_product {
	my $self = @_[0];
	my $name = @_[1];
	my $description = @_[2];
	my $query = @_[3];
	my $quantity = @_[4];
	my $flag = @_[5];
	$update_product_db->execute($name, $description, $query, $quantity, $flag, $query);
	$update_quantity->execute($query, $quantity);
	$self->print_info($query);
}

#add a new product
sub add_product {
	my $self = @_[0];
	my $name = @_[1];
	my $description = @_[2];
	my $query = @_[3];
	my $quantity = @_[4];
	my $flag = @_[5];
	$add_new_product->execute($name, $description, $query, $quantity, $flag);
	$update_quantity->execute($query, $quantity);
	$self->print_info($query);
}

#delete a product
sub delete_product {
	my $self = @_[0];
	my $barcode_val = @_[1];
	$self->print_info($barcode_val);
	$remove_product->execute($barcode_val);
}

#return all of the datapoints for a product for product use
sub return_log {
	my $query = @_[1];
	my $barcode;
	my $quantity;
	my $date;
	$get_stats->execute($query);
	$get_stats->bind_columns(undef, \$barcode, \$quantity, \$date);
	my @dates_ar;
	my @quantity_ar;
	while ($get_stats->fetch()) {
		push(@dates_ar, $date);
		push(@quantity_ar, $quantity);
	}
	my @array;
	push(@array, \@dates_ar);
	push(@array, \@quantity_ar);
	return $json->encode(\@array);
}

#return all the datapoints for a priduct for product use for a specific month (really not done yet)
sub gen_stats {
	my $self = @_[0];
	my $query = @_[1];
	my $barcode;
	my $quantity;
	my $date;
	my $d1 = DateTime->now;
	my @days;
	$get_stats->execute($query);
	$get_stats->bind_columns(undef, \$barcode, \$quantity, \$date);
	my @dates_ar;
	my @quantity_ar;
	while ($get_stats->fetch()) {
		push(@dates_ar, $date);
		push(@quantity_ar, $quantity);
	}
	print @dates_ar, " \= ", \@dates_ar, 'length=', length(@dates_ar), '<br>';
	for (my $i; $i <= length(@dates_ar); $i++) {
		my $d2 = DateTime::Format::MySQL->parse_datetime(\@dates_ar[$i]);
		my $day_dif = $d1->delta_days($d2), '<br>';
		print $day_dif, '<br>';
		push(@days, \$day_dif);
		
	}
	my $lineFit = Statistics::LineFit->new();
	$lineFit->setData (\@days, \@quantity_ar) or die "Invalid data";
	my ($intercept, $slope) = $lineFit->coefficients();
	print $intercept, $slope;
}

1;