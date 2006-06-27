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
        echo "<Page>";
        echo "\n<pidp>".$Temp[0]['ID']."</pidp>";
        echo "\n<title>".$Temp[0]['Title']."</title>";
        echo "\n<content>".htmlspecialchars($Temp[0]['Content'])."</content>";
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
        $Temp[0]['Content'] = $_POST['Content'] = html_entity_decode($_POST['Content']);
        $Temp[0]['Title']   = $_POST['Title'];

        if ($_POST['PageID']==0){
            $Values = Array ($_POST['Title'],$_POST['Content'],$_POST['Parent'],$_POST['Type']);
            $PP->InsertRecord($TableA,$Pages,$Values);
        }
        else {
            $PP->UpdateField($TableA,'Content',$_POST['Content'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Title',$_POST['Title'],$_POST['PageID']);
        }

        $Temp[0]['dblogs']=$PP->ShowLogs(1);
        ParseXML($Temp);
        die();
    }

    echo "<Info>NOT FOUND</Info>";

?>
