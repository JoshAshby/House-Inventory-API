package database;
use DBI;
use DBD::mysql;
use JSON;

my $json = new JSON;
   
do 'db_info.pl';

our $get_all_products;
our $get_product;
our $update_product_quantity;
our $add_new_product;
our $flag_set;
our $update_quantity;

sub new {
   my $class = shift;
   my $self = {};

   my $name;
   my $description;
   my $barcode;
   my $quantity;
   my $new_quantity;
   my $flag;
   my $average_days_left;
   my %text;

   bless ($self, $class);
   return $self;
}

sub print_info {
   my $query = @_[1];
   $get_product->execute($query,$query);
   $get_product->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
   my $p_text;
   while($get_product->fetch()){
      my %text = ('name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
      $p_text = $json->encode(\%text);
   }
   print $p_text;
}

sub total_inventory {
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
   my $query = @_[1];
   my $quantity = @_[2];
   $update_product_quantity->execute($quantity,$query,$query);
   $get_product->execute($query,$query);
   $get_product->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
   while($get_product->fetch()){
	$update_quantity->execute($barcode, $quantity)
  }
}

sub add_product {
    my $name = @_[1];
    my $description = @_[2];
    my $query = @_[3];
    my $quantity = @_[4];
    $add_new_product->execute($name, $description, $query, $quantity);
    $update_quantity->execute($query, $quantity)
}

sub remove_product {
    my $name = @_[1];
    $remove_product->execute($name);
}

1;
