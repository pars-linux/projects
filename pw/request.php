<?php
    
    # For requests
    # FIXME : Security 

    require_once ('config.php');
    require_once ('classes.php');
    
    $PP = new Pardus();
    $PP->DbLogDetail = $DbLogLevel;
    $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);

    header("Content-Type: application/xml; charset=UTF-8");
    echo   "<?xml version='1.0' standalone='yes'?>\n";
    
    function ParseXML($Temp) {
        echo "<Page>";
        echo "\n<pidp>".htmlspecialchars($Temp[0]['ID'])."</pidp>";
        echo "\n<title>".htmlspecialchars($Temp[0]['Title'])."</title>";
        echo "\n<content>".htmlspecialchars($Temp[0]['Content'])."</content>";
        echo "\n<dblog>".htmlspecialchars($Temp[0]['dblogs'])."</dblog>";
        echo "\n</Page>";
    }

    if (is_numeric($_GET['PageID'])) {
        $Temp = $PP->GetRecord($TableA,'*',$_GET['PageID']);
        $Temp[0]['dblogs']=$PP->ShowLogs(1);
        ParseXML($Temp);
        die();
    }
 
    if (is_numeric($_POST['PageID'])) {
        $PP->UpdateField($TableA,'Content',htmlspecialchars($_POST['Content'], ENT_QUOTES),$_POST['PageID']);
        $Temp[0]['Content'] = $_POST['Content'];
        $PP->UpdateField($TableA,'Title',$_POST['Title'],$_POST['PageID']);
        $Temp[0]['Title']   = $_POST['Title'];
        $Temp[0]['dblogs']=$PP->ShowLogs(1);
        ParseXML($Temp);
        die();
    }

    echo "<Info>NOT FOUND</Info>";

?>
