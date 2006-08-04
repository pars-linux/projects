<?php

    #Proc.php, panel's main actions

    #Start the session
    session_start();

    #Get configure file
    require_once ('../etc/config.php');

    #Check the session
    if (session_is_registered($SessionKeyword) AND $_SESSION['State']<=$SYS['TState']) {
        
        echo "<img src='".$_SESSION['UserPhoto']."' />"; 

    }
    else
        header("location: index.php");
?>
