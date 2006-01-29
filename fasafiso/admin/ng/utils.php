<?php

    require_once ("../../functions.php");

    /* Utils for FasaFiso Administration*/

    /* USERS - START */

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

    /* USERS - END */

    /* CATEGORIES - START */

    function get_categories(){
	global $config;
	$sql_word = "SELECT * FROM {$config['db']['tableprefix']}category ORDER BY id";
        return perform_sql($sql_word);
    }

    function add_category($category,$nicename,$description){
        global $config;
	$sql_word = "INSERT INTO {$config['db']['tableprefix']}category VALUES ('','{$category}', '{$nicename}', '{$description}')";
        return @mysql_query($sql_word);
    }

    function del_category($id){
        global $config;
	$sql_word = "DELETE FROM {$config['db']['tableprefix']}category WHERE id='{$id}'";
        return @mysql_query($sql_word);
    }

    function update_category($id,$category,$nicename,$description){
        global $config;
	$sql_word = "UPDATE {$config['db']['tableprefix']}category SET name='{$category}', nicename='{$nicename}', description='{$description}' WHERE id='$id'";
        return @mysql_query($sql_word);
    }

    /* CATEGORIES - END */
?>