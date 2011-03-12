#!/usr/bin/perl
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

use warnings;
use strict;

use CGI;
use DBI;
use DBD::mysql;
use JSON;

my $form=new CGI;
my $type_of_query=CGI::escapeHTML($form->param("type_of_query"));
my $query=CGI::escapeHTML($form->param("query"));

my $id;
my $name;
my $description;
my $barcode;
my $quantity;
my $new_quantity;
my %text;

our $get_product;
our $get_all_products;
our $update_product;

my $json = new JSON;

#do 'database.pl';

print $form->header();

if ($type_of_query eq 'single_product_info') {
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_product->fetch()){
      %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      print $json->encode(\%text);
   }
} elsif ($type_of_query eq 'total_inventory') {
   $get_all_products->execute();
   $get_all_products->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_all_products->fetch()){
      %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      print $json->encode(\%text);
   }
} elsif ($type_of_query eq 'update_product') {
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_product->fetch()){
      $new_quantity = $quantity + 1;
   }
   $update_product->execute("$new_quantity","$query","$query");
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_product->fetch()){
      %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      print $json->encode(\%text);
   }
}
