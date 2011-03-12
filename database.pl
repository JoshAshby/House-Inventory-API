our $platform = "mysql";
our $database = "pl_barcode";
our $host = "localhost";
our $port = "3306";
our $product_db = "products";
our $user = "root";
our $pw = "speeddyy5";
our $dsn = "dbi:$platform:$database:$host:$port";

our $connect = DBI->connect($dsn, $user, $pw) or die "Couldn't connect to database!" . DBI->errstr;

our $get_all_products = $connect->prepare_cached("SELECT * FROM $product_db ORDER BY id desc");

our $get_product = $connect->prepare_cached("SELECT * FROM $product_db WHERE name = ? OR barcode = ?");

our $update_product = $connect->prepare_cached(<<"SQL");
UPDATE $product_db
SET quanity = ?
WHERE name = ? OR barcode = ?
SQL
