package database;
use DBI;
use DBD::mysql;
use JSON;

my $json = new JSON;
   
do 'db_info.pl';

our $get_all_products;
our $get_product;
our $update_product;
our $add_new_product;

sub new {
   my $class = shift;
   my $self = {};

   my $id;
   my $name;
   my $description;
   my $barcode;
   my $quantity;
   my $new_quantity;
   my %text;
   my $p_text;

   bless ($self, $class);
   return $self;
}

sub print_info {
   my $query = shift;
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   my $p_text;
   while($get_product->fetch()){
      my %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      $p_text = $json->encode(\%text);
   }
   return $p_text;
}

sub total_inventory {
   $get_all_products->execute();
   $get_all_products->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   my @data_hash;
   while($get_all_products->fetch()){
      my %otext = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      push(@data_hash, \%otext);
   }
   print $json->encode(\@data_hash);
}

sub update_product_quantity {
   my $query = shift;
   my $quantity = shift;
   $update_product->execute("$quantity","$query","$query");
}

sub add_product {
    my $name = shift;
    my $description = shift;
    my $query = shift;
    my $quantity = shift;
    $add_new_product->execute("$name", "$description", "$query", "$quantity");
}

sub remove_product {
    my $name = shift;
    $remove_product->execute("$name");
}

1;
