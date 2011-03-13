our $platform = "mysql";
our $database = "joshashb_barcode";
our $host = "localhost";
our $port = "3306";
our $product_db = "products";
our $user = "joshashb_root";
our $pw = "speeddyy5";
our $dsn = "dbi:$platform:$database:$host:$port";

our $connect = DBI->connect($dsn, $user, $pw) or die "Couldn't connect to database!" . DBI->errstr;

our $get_all_products = $connect->prepare_cached("SELECT * FROM $product_db ORDER BY id desc");

our $get_product = $connect->prepare_cached("SELECT * FROM $product_db WHERE name = ? OR barcode = ?");

our $update_product = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET quantity = ?
WHERE name = ? OR barcode = ?
SQL

our $add_new_product = $connect->prepare_cached(<<"SQL");
INSERT INTO $comment_db
(id, name, description, barcode, quantity)
VALUES (?, ?, ?, ?, ?)
SQL
