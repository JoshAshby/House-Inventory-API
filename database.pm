package database;
use warnings;
use strict;
use DBI;
use DBD::mysql;
use JSON;

my $json = new JSON;
   
do 'db_info.pl';

our $get_all_products;
our $get_product_db;
our $add_new_product;
our $update_quantity;
our $remove_product;
our $get_stats;
our $update_product_db;

sub new {
	my $class = shift;
	my $self = {};

	bless ($self, $class);
	return $self;
}

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
	print $p_text;
}

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
	print $json->encode(\@data_hash);
}

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

sub delete_product {
	my $self = @_[0];
	my $barcode_val = @_[1];
	$self->print_info($barcode_val);
	$remove_product->execute($barcode_val);
}

sub return_log {
	my $query = @_[1];
	my $barcode;
	my $quantity;
	my $date;
	$get_stats->execute($query);
	$get_stats->bind_columns(undef, \$barcode, \$quantity, \$date);
	my %dates;
	my %quantity;
	my @dates_ar;
	my @quantity_ar;
	while ($get_stats->fetch()) {
		push(@dates_ar, $date);
		push(@quantity_ar, $quantity);
	}
	my @array;
	push(@array, \@dates_ar);
	push(@array, \@quantity_ar);
	print $json->encode(\@array);
}

1;