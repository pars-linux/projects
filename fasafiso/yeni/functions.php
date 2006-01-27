<?php
/*
Functions of Fasafiso
*/

    function db_connection($action, $dbhost = "", $dbuser = "", $dbpass = "", $dbname = "", $dbconntype = ""){
        global $db_connection;
        if($action == "connect"){
            if($dbconntype == "persistent"){$db_connection = @mysql_pconnect($dbhost, $dbuser, $dbpass);}
            elseif($dbconntype == "nonpersistent"){$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}
            else{$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}
            if(!$db_connection){
                db_error("Veritabanı sunucusuna bağlanamadım. Bir hata oluştu.", mysql_error(), mysql_errno());
                exit();
            }
            $db_select = @mysql_select_db($dbname);
            if(!$db_select){
                db_error("Veritabanına bağlantı kuramadım. Bir hata oluştu.", mysql_error(), mysql_errno());
                exit();
            }
        }
        elseif($action == "disconnect"){
            mysql_close($db_connection);
        }
        else{/* do nothing */}
    }

    function db_error($message,$mysql_message,$mysql_errno){
        echo $message."<br>";
        echo "Hata mesajı: <b>{$mysql_message}</b><br>";
        echo "Hata numarası: <b>{$mysql_errno}</b><br>";
        exit();
    }

    function set_smarty_vars($varname, $var){
        global $smarty;
        $smarty->assign($varname,$var);
    }

    function get_posts($id ="", $tags = "", $date = "", $author = "", $status = "", $startlimit = "", $endlimit = "", $conv_time = "db2post"){
        global $config;

        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}entry WHERE 1";

        if($id)$sql_word .= " AND id='{$id}'";
        //FIXME get by date?
        //if($date)$sql_word .= " AND date='{$date}'";
        if($author)$sql_word .= " AND author='{$author}'";
        if($status)$sql_word .= " AND status='{$status}'";
        $sql_word .= " ORDER BY 'date' DESC";
        if($startlimit<>"" AND $endlimit<>"")$sql_word .= " LIMIT {$startlimit} , {$endlimit}";

        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $return_array[$i]['category'] = get_cat($assoc_arr['id']);
            $return_array[$i]['date'] = conv_time($conv_time, $assoc_arr['date']);
            $return_array[$i]['author_id'] = $assoc_arr['author'];
            $tmp = get_user($assoc_arr['author'], "name");
            $return_array[$i]['author'] = $tmp[0]['name'];
            $return_array[$i]['comment_count'] = count_comments($assoc_arr['id']);
        }
        return $return_array;
    }

    function perform_sql($sql_word){
            $sql_query = mysql_query($sql_word);
            for($i = 0; $i < mysql_num_rows($sql_query); $i++){
                    $assoc_arr = mysql_fetch_assoc($sql_query);
                    $return[$i] = $assoc_arr;
            }
            if (empty($sql_query)) return 0;
            else return $return;
    }

    function rtag($foo){
        return htmlspecialchars($foo,ENT_QUOTES);
    }

    function sendmail($from,$to,$subject,$message,$priority){
           $mob = new Mail;
           $mob->From($from);
           $mob->To($to);
           $mob->Subject($subject);
           $mob->Body($message, "utf-8");
           $mob->Priority($priority);
           $mob->Send();
    }

    function conv_time($type,$value){
        if($type == "db2post"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $monthname = strftime("%B", strtotime("{$month}/01/{$year}"));
            $day = substr($value, 6, 2);
            $hour = substr($value, 8, 2);
            $minute = substr($value, 10, 2);
            $return_value = array("day" => $day, "month" => $month, "monthname" => $monthname, "year" => $year, "hour" => $hour, "minute" => $minute);
        }
        elseif($type == "db2rss"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $day = substr($value, 6, 2);
            $hour = substr($value, 8, 2);
            $minute = substr($value, 10, 2);
            $return_value = date("r", strtotime($year."-".$month."-".$day." ".$hour.":".$minute.":00"));
        }
        elseif($type == "db2archive"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $return_value = strftime("%B", strtotime("{$month}/01/{$year}"))."&nbsp;".$year;
        }
        return $return_value;
    }

    function count_comments($id){
        global $config;

        $sql_word = "SELECT id FROM {$config['db']['tableprefix']}comments WHERE entry_id='{$id}' AND status='1'";
        $sql_query = @mysql_query($sql_word);
        $return_string = @mysql_num_rows($sql_query);
        return $return_string;
    }


    function get_cat($id,$just=0,$reverse=0){
        global $config;
        if ($reverse) $sql_word = "SELECT * FROM {$config['db']['tableprefix']}category_act WHERE cat_id = '$id'";
        else $sql_word = "SELECT * FROM {$config['db']['tableprefix']}category_act WHERE entry_id = '$id'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
                $assoc_arr = mysql_fetch_assoc($sql_query);
                if ($reverse) $return_array[$i] = $assoc_arr['entry_id'];
                if ($just==1) $return_array[$i] = $assoc_arr['cat_id'];
                elseif ($reverse==0) {
                $return_array[$i] = $assoc_arr;
                $return_array[$i]['name'] = get_category_name($assoc_arr['cat_id']);
                }
        }
        return $return_array;
    }

    function get_archives($uid=""){
        global $config;
        if ($uid) {$act="WHERE author='{$uid}'";$act2="AND author='{$uid}'";}
        else {$act="WHERE status='1'";$act2="AND status='1'";}
        $sql_word = "SELECT DISTINCT SUBSTRING(`date`,1,6) FROM {$config['db']['tableprefix']}entry ".$act." ORDER by date DESC";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
                $assoc_arr = mysql_fetch_assoc($sql_query);
                //$return_array[$i] = $assoc_arr;
                $return_array[$i]['date'] = $assoc_arr['SUBSTRING(`date`,1,6)'];
                $return_array[$i]['name'] = conv_time("db2archive", $assoc_arr['SUBSTRING(`date`,1,6)']);
                $sql_word_fsfs = "SELECT date FROM {$config['db']['tableprefix']}entry WHERE date LIKE '{$assoc_arr['SUBSTRING(`date`,1,6)']}%' ".$act2;
                $sql_query_fsfs = @mysql_query($sql_word_fsfs);
                $number = @mysql_num_rows($sql_query_fsfs);
                $return_array[$i]['count'] = $number;
        }
        return $return_array;
    }

    function get_categories($id = ""){
        global $config;

        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}category";
        $sql_query = @mysql_query($sql_word);

        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $sql_word_fsfs = "SELECT id FROM {$config['db']['tableprefix']}category_act WHERE cat_id='{$assoc_arr['id']}'";
            $sql_query_fsfs = @mysql_query($sql_word_fsfs);
            $number = @mysql_num_rows($sql_query_fsfs);
            $return_array[$i]['count'] = $number;
            // there is a bug in counting but itsn't important
            // now it shows draft or published writes count
        }
        return $return_array;
    }


    function get_comments($id = "", $entry_id = "", $status = "1", $conv_time = "db2post"){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}comments WHERE 1 AND ";
        if($status != ""){$sql_word .= "status='{$status}' AND ";}
        if($id AND $id != ""){
            $sql_word .= " id='{$id}'";
        }
        if($entry_id AND $entry_id != ""){
            $sql_word .= " entry_id='{$entry_id}'";
        }
            $sql_word .= " ORDER BY 'date' ASC";

        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
                $assoc_arr = mysql_fetch_assoc($sql_query);
                $return_array[$i] = $assoc_arr;
                $return_array[$i]['email'] = str_replace("@", " ¤ ", $return_array[$i]['email']);
                $return_array[$i]['email'] = str_replace(".", " · ", $return_array[$i]['email']);
                $return_array[$i]['date'] = conv_time($conv_time, $assoc_arr['date']);
        }
        return $return_array;
    }

    function get_category_name($id){
        global $config;

        $sql_word = "SELECT name FROM {$config['db']['tableprefix']}category WHERE id='{$id}'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_string = $assoc_arr['name'];
        }
        return $return_string;
    }

    function get_user($id,$thing,$opt="") {
        global $config;
        if ($opt=="username") $attach_sql = " username = '$id'"; else $attach_sql = " id = '$id'";
        $sql_word = "SELECT $thing FROM {$config['db']['tableprefix']}users WHERE".$attach_sql;
        return perform_sql($sql_word);
    }

    function get_links($id=""){
        global $config;
        if($id){$act = "WHERE id='{$id}'";}
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}links ".$act;
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
                $assoc_arr = mysql_fetch_assoc($sql_query);
                $return_array[$i] = $assoc_arr;
        }
        return $return_array;
    }
?>
