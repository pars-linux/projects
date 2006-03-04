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

    /* ENTRIES - START */

    function get_entry($id){
        global $config;
	$sql_word = "SELECT * FROM {$config['db']['tableprefix']}entry WHERE id = '$id'";
        return perform_sql($sql_word);
    }

    function get_entries($userid,$date=""){
        global $config;

        $date <> "" ? $sql_add=" date LIKE '{$date}%' AND " : $sql_add="";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}entry WHERE ".$sql_add." author = '$userid'";
        return perform_sql($sql_word);
    }

    function get_entries_by_month($userid){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}entry WHERE ".$sql_add." author = '$userid'";
        return perform_sql($sql_word);
    }
    
    function add_entry($userid,$title,$entry,$date,$categories,$state){
        global $config;
        $sql_word = "INSERT INTO {$config['db']['tableprefix']}entry VALUES ('','{$title}', '{$entry}', '{$date}', '{$userid}', '{$state}')";
        if (!(@mysql_query($sql_word))) return FALSE;
        else link_category_entry($categories,mysql_insert_id());
        return mysql_insert_id();
    }

    function del_entry($userid,$id){
        global $config;

    }

    function update_entry($id,$title,$entry,$date,$categories,$state){
        global $config;
	$sql_word = "UPDATE {$config['db']['tableprefix']}entry SET title='{$title}', entry='{$entry}', date='{$date}', status='{$state}' WHERE id='$id'";
        if (!(@mysql_query($sql_word))) return FALSE;
        else link_category_entry($categories,$id);
        return $id;
    }

    function link_category_entry($cat_id,$entry_id){
	global $config;
        $sql_word = "DELETE FROM {$config['db']['tableprefix']}category_act WHERE entry_id='{$entry_id}'";
        $sql_query = @mysql_query($sql_word);
        if ($cat_id):
	foreach ($cat_id as $cat) {
            $sql_word = "INSERT INTO {$config['db']['tableprefix']}category_act VALUES ('', '{$cat}', '{$entry_id}')";
	    $sql_query = @mysql_query($sql_word);
	}
        endif;
    }

    function get_entry_categories($id){
        global $config;
	$sql_word = "SELECT * FROM {$config['db']['tableprefix']}category_act WHERE entry_id = '$id'";
        return perform_sql($sql_word);
    }

    /* ENTRIES - END */

?>
