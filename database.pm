package database;
use DBI;
use DBD::mysql;
use JSON;

my $json = new JSON;
   
do 'db_info.pl';

our $get_all_products;
our $get_product_db;
our $update_product_quantity;
our $add_new_product;
our $flag_set;
our $update_quantity;
our $remove_product;

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
   $get_product_db->execute($query,$query);
   $get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
   my $p_text;
   while($get_product_db->fetch()){
	$update_quantity->execute($barcode, $quantity);
	my %text = ('change' => 'update', 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
       $p_text = $json->encode(\%text);
  }
  print $p_text;
}

sub update_product_info {
    my $name = @_[1];
    my $description = @_[2];
    my $query = @_[3];
    my $quantity = @_[4];
    $update_product->execute($name, $description, $query, $quantity, $query);
    $update_quantity->execute($query, $quantity);
    $get_product_db->execute($query,$query);
    $get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
    my $p_text;
    while($get_product_db->fetch()){
       my %text = ('change' => 'update', 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
       $p_text = $json->encode(\%text);
    }
    print $p_text;
}

sub add_product {
    my $name = @_[1];
    my $description = @_[2];
    my $query = @_[3];
    my $quantity = @_[4];
    $add_new_product->execute($name, $description, $query, $quantity);
    $update_quantity->execute($query, $quantity);
    $get_product_db->execute($query,$query);
    $get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
    my $p_text;
    while($get_product_db->fetch()){
       my %text = ('change' => 'added', 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
       $p_text = $json->encode(\%text);
    }
    print $p_text;
}

sub delete_product {
    my $barcode_val = @_[1];
    $get_product_db->execute($barcode_val,$barcode_val);
    $get_product_db->bind_columns(undef, \$name, \$description, \$barcode, \$quantity, \$flag, \$average_days_left);
    my $p_text;
    while($get_product_db->fetch()){
      my %text = ('change' => 'removed', 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity, 'flag' => $flag, 'average' => $average_days_left);
      $p_text = $json->encode(\%text);
   }
   print $p_text;
   $remove_product->execute($barcode_val);
}

1;