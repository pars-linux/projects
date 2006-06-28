<?php

    # For requests
    # FIXME : Security

    require_once ('config.php');
    require_once ('classes.php');

    $PP = new Pardus();
    $PP->DbLogDetail = $DbLogLevel;
    $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);

    if (is_numeric($_GET['PageID']))
        $Temp = $PP->GetRecord($TableA,'*',$_GET['PageID']);
    if (isset($_GET['Title']))
        $Temp = $PP->GetRecordByTitle($TableA,'*',$_GET['Title']);

    if ($Temp) {
        echo $Temp[0]['Content'];
    }

?>
