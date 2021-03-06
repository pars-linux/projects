<?php

    /*
        db_connection();
    */
    function db_connection($action, $dbhost = "", $dbuser = "", $dbpass = "", $dbname = "", $dbconntype = ""){
        global $db_connection;
        if($action == "connect"){
            if($dbconntype == "persistent"){$db_connection = @mysql_pconnect($dbhost, $dbuser, $dbpass);}
            elseif($dbconntype == "nonpersistent"){$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}
            else{$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}
            if(!$db_connection){ show_mysql_errors(); exit();}
            $db_select = @mysql_select_db($dbname);
            if(!$db_select){ show_mysql_errors(); exit();}
        }
        elseif($action == "disconnect"){mysql_close($db_connection);}
    }

    /*
        show_mysql_errors()
        It shows nice mysql errors
        return No_Return;
    */
    function show_mysql_errors() {
            echo DBCONERROR."<br>";
            echo ERRORMESSAGE."<b>".mysql_error()."</b><br>";
            echo ERRORNUM."<b>".mysql_errno()."</b><br>";
    }

    /*
        perform_sql()
    */
    function perform_sql($sql_word){
            $sql_query = mysql_query($sql_word);
            for($i = 0; $i < mysql_num_rows($sql_query); $i++){
                    $assoc_arr = mysql_fetch_assoc($sql_query);
                    $return[$i] = $assoc_arr;
            }
            if (empty($sql_query)) return 0;
            else return $return;
    }

    /*
        set_smarty_vars($varname, $var)
        It makes variable for using in smarty (in theme files)
        return No_Return;
    */
    function set_smarty_vars($varname, $var){
            global $smarty;
            $smarty->assign($varname,$var);
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

?>