<?php
    
    # For requests
    # FIXME : Security 

    header("Content-Type: application/xml; charset=UTF-8");

    echo "<?xml version='1.0' standalone='yes'?>\n";

    if ($_GET['PageID']<>"") {
        echo "<Page>\n";
        require_once ('config.php');
        require_once ('classes.php');

        $PP = new Pardus();
        $PP->DbLogDetail = $DbLogLevel;
        $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);
        $Temp = $PP->GetRecord($TableA,'Content',$_GET['PageID']);
        echo "<content>\n".htmlspecialchars($Temp[0]['Content'])."\n</content>";
        echo "\n<dblog>".htmlspecialchars($PP->ShowLogs(1))."\n</dblog>\n</Page>";
    }

?>
