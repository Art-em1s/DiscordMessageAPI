<?php
$db = new SQLite3("/path/to/database.db");
$out = array();
if ($_GET){
    if($_GET["page"]){
        if (!is_int($_GET["page"])||$_GET["page"]<0){
            $page = 0; #account for people trying to break shit
        } else {
            $page = $_GET["page"]*50;
        }
    } else {
        $page = 0;
    }
} else {
    $page = 0;
}
$sql = "select messages.time,messages.message,messages.user,users.name,users.discrim,users.avatar,users.color from messages left join users where users.user == messages.user limit 50 offset  $page";
$res = $db->query($sql);
while ($row = $res->fetchArray()) {
    $row = array(
    "epoch" => $row[0],
    "message" => $row[1],
    "user_id" => $row[2],
    "name" => $row[3],
    "discrim" => $row[4],
    "avatar" => $row[5],
    "color" => $row[6]);
    $out[] = $row;
}
echo json_encode($out);
?>