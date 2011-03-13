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
my $query_value=CGI::escapeHTML($form->param("query"));
my $quantity_value=CGI::escapeHTML($form->param("quantity"));

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

do 'database.pl';

sub print_single_info {
   my $query = shift;
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_product->fetch()){
      %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      print $json->encode(\%text);
   }
};

sub print_total_inventory {
   $get_all_products->execute();
   $get_all_products->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_all_products->fetch()){
      %text = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      print $json->encode(\%text);
   }
};

sub update_single_product {
   my $query = shift;
   $get_product->execute("$query","$query");
   $get_product->bind_columns(undef, \$id, \$name, \$description, \$barcode, \$quantity);
   while($get_product->fetch()){
      $new_quantity = $quantity + 1;
   }
   $update_product->execute("$new_quantity","$query","$query");
};

sub update_single_product_quantity {
   my $query = shift;
   my $quantity = shift;
   $update_product->execute("$quantity","$query","$query");
};


print $form->header();

if ($type_of_query eq 'single_product_info') {
   print_single_info($query_value);
} elsif ($type_of_query eq 'total_inventory') {
   print_total_inventory();
} elsif ($type_of_query eq 'update_product') {
   update_single_product();
   print_single_info($query_value);
} elsif ($type_of_query eq 'update_product_quantity') {
   update_single_product_quantity($query_value, $quantity_value);
   print_single_info($query_value);
}
