my $platform = "mysql";
my $database = "pl_barcode";
my $host = "localhost";
my $port = "3306";
my $product_db = "products";
my $stats_db = "stats";
my $user = "root";
my $pw = "speeddyy5";
my $dsn = "dbi:$platform:$database:$host:$port";

my $connect = DBI->connect($dsn, $user, $pw) or die "Couldn't connect to database!" . DBI->errstr;

our $get_all_products = $connect->prepare_cached(<<"SQL");
SELECT name, description, barcode, quantity, flag
FROM $product_db
ORDER BY id desc
SQL

our $remove_product = $connect->prepare_cached(<<"SQL");
DELETE FROM $product_db
WHERE barcode = ?
SQL

our $get_product_db = $connect->prepare_cached(<<"SQL");
SELECT name, description, barcode, quantity, flag, average
FROM $product_db
WHERE name = ? OR barcode = ?
SQL

our $update_product_quantity = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET quantity = ?
WHERE name = ? OR barcode = ?
SQL

our $update_product = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET name = ?, description = ?, barcode = ?, quantity = ?
WHERE barcode = ?
SQL

our $add_new_product = $connect->prepare_cached(<<"SQL");
INSERT INTO $product_db
(name, description, barcode, quantity, flag)
VALUES (?, ?, ?, ?, ?)
SQL

our $flag_set = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET flag = ?
WHERE name = ? OR barcode = ?
SQL

our $update_quantity = $connect->prepare_cached(<<"SQL");
INSERT INTO $stats_db
(barcode, quantity)
VALUES (?, ?)
SQL

our $gen_stats = $connect->prepare_cached(<<"SQL");
SELECT *
FROM $stats_db
WHERE barcode = ?
ORDER BY date desc
SQL
