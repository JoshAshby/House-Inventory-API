my $platform = "mysql";
my $database = "pl_barcode";
my $host = "localhost";
my $port = "3306";
my $product_db = "products";
my $user = "root";
my $pw = "speeddyy5";
my $dsn = "dbi:$platform:$database:$host:$port";

my $connect = DBI->connect($dsn, $user, $pw) or die "Couldn't connect to database!" . DBI->errstr;

our $get_all_products = $connect->prepare_cached("SELECT * FROM $product_db ORDER BY id desc");

our $get_product = $connect->prepare_cached("SELECT * FROM $product_db WHERE name = ? OR barcode = ?");

our $update_product = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET quantity = ?
WHERE name = ? OR barcode = ?
SQL

our $add_new_product = $connect->prepare_cached(<<"SQL");
INSERT INTO $product_db
(name, description, barcode, quantity)
VALUES (?, ?, ?, ?)
SQL
