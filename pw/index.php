<?php

    session_start();

    session_unregister($SessionKeyword);

    $_SESSION['state']="";
    $_SESSION['loginName']="";

    if (array_key_exists('login',$_GET)) {

        require_once ('config.php');
        require_once ('classes.php');

        $PP = new Pardus();
        $PP->DbLogDetail = $DbLogLevel;
        $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);

        if ($Temp=$PP->GetUserDetails($_POST['username'],$_POST['password'])) {
            session_register($SessionKeyword);
            $_SESSION['state'] = $Temp[0]['UserState'];
            $_SESSION['loginName'] = $Temp[0]['UserRealName'];
            header("location: proc.php");
        }
        else
            $Message = "Kullanıcı Adı veya Parola Hatalı !";
    }

?>

    <html>
    <head>
    <title>PardusOrgTr</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="stil.css" rel="stylesheet" type="text/css">
    </head>

    <body>
    <form method="post" action="?login">
    <div id="loginPane">
        <div id="loginNodes">
            <div class="username">
            <label for="username">Kullanıcı Adı</label>

            <input name="username" id="username" type="text" maxlength="10" class="txt" />
            </div>

            <div class="password">
            <label for="password">Parola</label>
            <input name="password" id="password" type="password" class="txt pwd" /><br />
            </div>

            <div class="buttons">
            <input type="submit" value="Giriş" alt="login" name="login" class="button"/>
            </div>
            <?php if ($Message) { ?>
                <div class="infoLogin">
                    <span class="error"><?=$Message?></span>
                </div>
            <?php } ?>
        </div>
    </div>

    </form>
    </body>
    </html>
