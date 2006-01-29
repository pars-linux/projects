<?php

    require_once ("../../functions.php");

    /* Utils for FasaFiso Administration*/

    function get_user_details($user,$passo,$state=FALSE){
        global $config;
        $uname = $passo;
        $pass = md5($passo);
        if ($state<>4) $attach_sql =" AND status = '{$state}'";
        if ($user<>"") $attach_sql .=" AND id = '{$user}'";
        if (!$state) $sql_word = "SELECT * FROM {$config['db']['tableprefix']}users WHERE username = '$user' AND passwd = '$pass' AND status != '3'";
        else $sql_word = "SELECT * FROM {$config['db']['tableprefix']}users WHERE username = '$uname'".$attach_sql;
        return perform_sql($sql_word);
    }

    function get_categories(){
	global $config;
	$sql_word = "SELECT * FROM {$config['db']['tableprefix']}category";
        return perform_sql($sql_word);
    }

?>