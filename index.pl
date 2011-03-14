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
my $description_value=CGI::escapeHTML($form->param("description"));
my $name_value=CGI::escapeHTML($form->param("name"));
my $quantity_value=CGI::escapeHTML($form->param("quantity"));

my $id;
my $name;
my $description;
my $barcode;
my $quantity;
my $new_quantity;
my %text;
my @ptext;

our $get_product;
our $get_all_products;
our $update_product;
our $add_new_product;

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
   my @data_hash;
   while($get_all_products->fetch()){
      my %otext = ('id' => $id, 'name' => $name, 'description' => $description, 'barcode' => $barcode, 'quantity' => $quantity);
      push(@data_hash, \%otext);
   }
   print $json->encode(\@data_hash);
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

sub add_new_product {
    my $name = shift;
    my $description = shift;
    my $query = shift;
    my $quantity = shift;
    $add_new_product->execute("$name", "$description", "$query", "$quantity");
}


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
} elsif ($type_of_query eq 'add_new_product') {
   add_new_product($name_value, $description_value, $query_value, $quantity_value);
   print_single_info($name_value);
}
