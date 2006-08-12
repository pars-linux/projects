<?php

    #Start the session
    session_start();

    #Get Config and Set Lang vars
    require_once ('../etc/config.php');
    require_once ('../lang/'.$LF); 

    #Cleanup old sessions
    session_unregister($SessionKeyword);
    $_SESSION['state']="";
    $_SESSION['loginName']="";

    #Check Login or not
    if (array_key_exists('login',$_GET)) {

        #if Login, get sysvars and connection functions
        require_once ('../etc/sysvars.php');
        require_once ('../lib/vezir.php');

        #create an instance for connection to database
        $Vezir = new Vezir($CF);

        #Check user and set session if ok
        if ($Temp=$Vezir->GetUserDetails('Users',$_POST['username'],$_POST['password'],false)) {
            session_register($SessionKeyword);
            $_SESSION['Status'] = $Temp[0]['Status'];
            $_SESSION['UserName'] = $Temp[0]['UserName'];
            $_SESSION['RealName'] = $Temp[0]['RealName'];
            $_SESSION['UserPhoto'] = $Temp[0]['PhotoLink'];
            header("location: {$SYS['ProcFile']}");
        }

        #if wrong info given set message to warn user
        else
            $Message = USERNAME_OR_PASSWORD_WRONG;
    }

    #if any Vezir errors show them.
    if ($Vezir)
        $Vezir->ShowLogs();

    #Get template file
    include_once('template/login/index.tmpl');

?>
