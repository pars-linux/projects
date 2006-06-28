<?php

    # For requests
    # FIXME : Security

    require_once ('config.php');
    require_once ('classes.php');

    $PP = new Pardus();
    $PP->DbLogDetail = $DbLogLevel;
    $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);

    if (isset($_GET['PageList'])){
        PageList(PrettyList($PP->GetRecord($TableA,'*')));
        die();
    }

    header("Content-Type: application/xml; charset=UTF-8");
    echo   "<?xml version='1.0' standalone='yes'?>\n";

    function ParseXML($Temp) {
        global $Parents,$Ptypes;
        echo "<Page>";
        echo "\n<pidp>".$Temp[0]['ID']."</pidp>";
        echo "\n<title>".$Temp[0]['Title']."</title>";
        echo "\n<content>".htmlspecialchars($Temp[0]['Content'])."</content>";
        echo "\n<parent>".array_search($Temp[0]['Parent'],$Parents)."</parent>";
        echo "\n<ptype>".array_search($Temp[0]['PType'],$Ptypes)."</ptype>";
        echo "\n<dblog>".htmlspecialchars($Temp[0]['dblogs'])."</dblog>";
        echo "\n</Page>";
    }

    if (is_numeric($_GET['PageID'])) {
        $Temp = $PP->GetRecord($TableA,'*',$_GET['PageID']);
        if ($Temp) {
            $Temp[0]['dblogs']=$PP->ShowLogs(1);
            ParseXML($Temp);
            die();
        }
    }

    if (is_numeric($_POST['PageID'])) {
        $_POST['Content'] = html_entity_decode($_POST['Content']);
        
        if ($_POST['PageID']==0){
            $Values = Array ($_POST['Title'],$_POST['Content'],$_POST['Parent'],$_POST['PType']);
            $TID = $PP->InsertRecord($TableA,$Pages,$Values);
            $Temp = $PP->GetRecord($TableA,'*',$TID);
        }
        else {
            $PP->UpdateField($TableA,'Content',$_POST['Content'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Title',$_POST['Title'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Parent',$_POST['Parent'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Ptype',$_POST['Ptype'],$_POST['PageID']);
            $Temp = $PP->GetRecord($TableA,'*',$_POST['PageID']);
        }

        $Temp[0]['dblogs']=$PP->ShowLogs(1);
        ParseXML($Temp);
        die();
    }

    echo "<Info>NOT FOUND</Info>";

?>
