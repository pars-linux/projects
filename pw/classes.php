<?php

    // Gökmen GÖKSEL gokmen<at>pardus.org.tr
    // TUBITAK/UEKAE :: Pardus W Classes

        class Pardus {
           
            private $Connection;
            
            // 0 - to don't show any message.
            // 2 - to just show errors.
            // 3 - to show all actions.
            public $DbLogDetail;

            function DbConnect($DbHost,$DbUser,$DbPass,$DbData){   
                try {
                    $this->Connection = @mysql_connect($DbHost,$DbUser,$DbPass,$DbData);
                    if (!$this->Connection)
                        throw new Exception('Connection Error',2);
                    elseif ($this->DbLogDetail>3)
                        $this->ParseError("Connected to $DbHost::$DbData");
                    mysql_select_db($DbData);
                }

                catch (Exception $Ex) {
                    $this->ShowError($Ex);
                    exit();
                } 
            }

            function ShowError($Ex,$Note='') { 
                if ($this->DbLogDetail>1) {
                    echo '<pre><b>';
                    echo 'DEBUG: Exception '.$Ex->getCode().' : '.$Ex->getMessage()."<br>";
                    echo 'DEBUG: File        : '.$Ex->getFile().' : '.$Ex->getLine()."<br>";
                    if ($Note<>"") echo 'DEBUG: Note        : '.$Note.'<br>';
                    echo 'DEBUG: Exiting...';
                    echo '</b></pre>';
                }
                else $this->ParseError("An error occured. Exiting..");
            }

            function UpdateField($Table,$Field,$Value,$ID='') {
                $ID == "" ? $AddSql = "" : $AddSql = "WHERE ID=$ID";
                $Sql = "UPDATE $Table SET $Field='$Value' ".$AddSql;
                $this->ExecuteQuery($Sql);               
            }
            
            function InsertRecord($Table,$Fields,$Values) {
                $Sql = "INSERT INTO $Table (";
                foreach ($Fields as $FValue) {
                    $Sql .= $FValue.",";
                }
                $Sql = rtrim($Sql,",");
                $Sql .= ") VALUES (";
                foreach ($Values as $VValue) {
                    $Sql .= "'".$VValue."'".",";
                }
                $Sql = rtrim($Sql,",");
                $Sql .=")";
                $this->ExecuteQuery($Sql);
                return mysql_insert_id();
            }

            protected function ExecuteQuery($Sql) {
                try {
                    $Result = mysql_query($Sql,$this->Connection);
                    if (!$Result)
                        throw new Exception('Query Execution Error',3);
                    elseif ($this->DbLogDetail>2)
                        $this->ParseError("Query Executed Sucessfully : ".$Sql);
                    return $Result;
                }
                catch (Exception $Ex) {
                    $this->ShowError($Ex,$Sql);
                    return false;
                }
            }

            function ParseError($Message) {
                $this->MessageQueue.= "<pre><b>DEBUG : ".$Message."</b></pre>";
            }

            function GetRecord($Table,$Field='*',$ID='') {
                $ID == "" ? $AddSql = "" : $AddSql = "WHERE ID=$ID";
                $Sql = "SELECT $Field FROM $Table ".$AddSql;
                $Result = $this->ExecuteQuery($Sql);
                return $this->MakeArray($Result);
            }

            function FindRecord($Table,$Field,$Value,$ReturnValue='ID') {
                $Sql = "SELECT $ReturnValue FROM $Table WHERE $Field LIKE '%$Value%'";
                $Result = $this->ExecuteQuery($Sql);
                return $this->MakeArray($Result);
            }

            function MakeArray($Raw) {
                $i=0;
                while ($Row = mysql_fetch_array($Raw, MYSQL_ASSOC)) {
                    foreach ($Row as $RKey => $RValue)
                        $ReturnValue[$i][$RKey] = $RValue;
                    $i++;
                }
                if ($i==0)
                    $ReturnValue = 0;
                mysql_free_result($Raw);
                return $ReturnValue;
            }

            function ShowLogs($Opt=0) {
                if ($Opt)
                    return $this->MessageQueue;
                else
                    echo $this->MessageQueue;
            }
        }

        # i know it sucks.
        function PrettyList($Array) {
            $i=0;
            foreach ($Array as $Value) {
                $Value['Title'] = substr($Value['Title'], 0, 22).'..';
                $ReturnArray[$i] = $Value;
                $i++;
            }
            return $ReturnArray;
        }

        function JsLink($ID,$Value,$Action) {
            return '<a href=# onClick="'.$Action.'(\''.$ID.'\')">'.$Value.'</a>';  
        }

        function PageList($PageList){
            foreach ($PageList as $Key=>$Value) {
                echo '<div class="';
                echo (($Key+1)%2)? 'koyu' : 'acik';
                echo '">';
                echo ($Key+1).'::';
                echo '<b>'.$Value['Parent'].'</b>::';
                echo JsLink($Value['ID'],$Value['Title'],'Edit');
                echo '</div>';
            }
        }
?>
