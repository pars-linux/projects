<?php

    # For requests
    # FIXME : Security

    session_start();

    require_once ('config.php');

    if (session_is_registered($SessionKeyword) AND $_SESSION['state']=="A") {

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
        global $Parents,$Ptypes,$Plangs;
        echo "<Page>";
        echo "\n<pidp>".$Temp[0]['ID']."</pidp>";
        echo "\n<title>".$Temp[0]['Title']."</title>";
        echo "\n<ntitle>".$Temp[0]['NiceTitle']."</ntitle>";
        echo "\n<modules>".$Temp[0]['Modules']."</modules>";
        echo "\n<content>".htmlspecialchars($Temp[0]['Content'])."</content>";
        echo "\n<plang>".array_search($Temp[0]['Lang'],$Plangs)."</plang>";
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
        $_POST["Modules"]=strtoupper($_POST["Modules"]);
        if ($_POST['PageID']==0){
            $Values = Array ($_POST['Title'],$_POST['NiceTitle'],$_POST['Content'],$_POST['Modules'],$_POST['Plang']);
            $TID = $PP->InsertRecord($TableA,$Pages,$Values);
            $Temp = $PP->GetRecord($TableA,'*',$TID);
        }
        else {
            $PP->UpdateField($TableA,'Content',$_POST['Content'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Title',$_POST['Title'],$_POST['PageID']);
            $PP->UpdateField($TableA,'NiceTitle',$_POST['NiceTitle'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Modules',$_POST['Modules'],$_POST['PageID']);
            $PP->UpdateField($TableA,'Lang',$_POST['Plang'],$_POST['PageID']);
            $Temp = $PP->GetRecord($TableA,'*',$_POST['PageID']);
        }

        $Temp[0]['dblogs']=$PP->ShowLogs(1);
        ParseXML($Temp);
        die();
    }

    if (is_numeric($_POST['Delete'])){
            $PP->DeleteRecord($TableA,$_POST['Delete']);
            if ($DbLogLevel>2)
                echo "<b>".$_POST['Delete']." ID 'li kayıt silindi.</b>";
            die();
    }

        echo "<Info>NOT FOUND</Info>";
        die();
    }
    else
        header("location: index.php");
?>
