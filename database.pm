package database;
use warnings;
use strict;
use DBI;
use DBD::mysql;
use JSON;
use DateTime;
use DateTime::Format::MySQL;
use DateTime::Format::Duration;

my $json = new JSON;
   
do 'db_info.pl';

our $get_all_products;
our $get_product_db;
our $update_product_quantity;
our $add_new_product;
our $flag_set;
our $update_quantity;
our $remove_product;
our $gen_stats;
our $average_set;
our $update_product;

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

sub return_quantity {
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
		return $quantity;
	}
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

sub update_product_quantity {
	my $self = @_[0];
	my $query = @_[1];
	my $quantity = @_[2];
	$update_product_quantity->execute($quantity,$query,$query);
	$self->print_info($query);
}

sub update_product_info {
	my $self = @_[0];
	my $name = @_[1];
	my $description = @_[2];
	my $query = @_[3];
	my $quantity = @_[4];
	$update_product->execute($name, $description, $query, $quantity, $query);
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
	$gen_stats->execute($query);
	$gen_stats->bind_columns(undef, \$barcode, \$quantity, \$date);
	my %dates;
	my %quantity;
	my @dates_ar;
	my @quantity_ar;
	while ($gen_stats->fetch()) {
		push(@dates_ar, $date);
		push(@quantity_ar, $quantity);
	}
	my @array;
	push(@array, \@dates_ar);
	push(@array, \@quantity_ar);
	print $json->encode(\@array);
}

sub gen_stat {
	my $self = @_[0];
	my $barcode_val = @_[1];
	my $name;
	my $description;
	my $barcode;
	my $quantity;
	my $new_quantity;
	my $flag;
	my $average_days_left;
	my $date;
	$gen_stats->execute($barcode_val);
	$gen_stats->bind_columns(undef, \$barcode, \$quantity, \$date);
	my @dates;
	my @quantity;
	while ($gen_stats->fetch()) {
		push(@dates, $date);
		push(@quantity, $quantity);
	}
	my $count;
	my $average;
	for ($count = 1; $count <= 4; $count++) {
		my $d1 = DateTime::Format::MySQL->parse_datetime(@dates[$count]);
		my $d2 = DateTime::Format::MySQL->parse_datetime(@dates[$count-1]);
		my $duration = $d2 - $d1;
		my $format = DateTime::Format::Duration->new(
			pattern => '%e'
		);
		print int($format->format_duration($duration));
		$average += int($format->format_duration($duration));
	}
	print $average;
	$average = $average/10;
	print $average;
	my $data = @quantity[0];
	my $d1 = DateTime->now();
	my $d2 = DateTime::Format::MySQL->parse_datetime(@dates[0]);
	my $duration = $d2 - $d1;
	my $format = DateTime::Format::Duration->new(
		pattern => '%e'
	);
	my $time = $data-int($format->format_duration($duration));
	$average_set->execute($average, $barcode_val, $barcode_val);
	if ($time <= 10 && $time > 5) {
		$flag_set->execute('M', $barcode_val, $barcode_val);
	} elsif ($time <= 5 && $time >= 0) {
		$flag_set->execute('H', $barcode_val, $barcode_val);
	} elsif ($time > 10) {
		$flag_set->execute('L', $barcode_val, $barcode_val);
	}
}

1;