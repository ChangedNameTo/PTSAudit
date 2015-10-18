<?php
$host = "159.203.104.66";
$user = "root";
$pass = "appathon;

$databaseName = "rambler";
$con=mysql_connect($host, $user, $pass);
$tableName = "rambler";
if(!$con)
{
    die('Could not connect: ' . mysql_error());
}

$dbs = mysql_select_db($databaseName, $con);

$result = mysql_query("SELECT * FROM $tableName");
$array = mysql_fetch_row($result);

echo json_encode($array);
?>
