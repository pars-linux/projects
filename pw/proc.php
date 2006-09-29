<?php

    session_start();

    require_once ('config.php');

    if (session_is_registered($SessionKeyword) AND $_SESSION['state']=="A") {
    require_once ('classes.php');

    $PP = new Pardus();
    $PP->DbLogDetail = $DbLogLevel;
    $PP->DbConnect($DbHost,$DbUser,$DbPass,$DbData);

?>

    <html>
    <head>
    <title>PardusOrgTr</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="stil.css" rel="stylesheet" type="text/css">
    <script src="scripts/prototype.js"></script>
    <script src="scripts/script.php"></script>
    </head>

    <body onLoad="ClearFields();ShowPageList();" class="Pbody">

    <div id="over" style="display:none">
        <div style="padding-top:25%;color:#FFF;">
            <img src="images/spin.gif"/>
            <br>çalışıyor
        </div>
    </div>

    <div id="htmleditor" style="display:none"></div>

    <center>

    <!-- Content -->

    <table style="height:100%;">
    <tr>
        <td id="header">
            <div id="menu">
                <span style="float:left">
                    <a href="#" onClick="AddNewPage()">Yeni Ekle</a>||
                    <a href="#" onClick="ToggleHTML()">HTML Olarak Göster</a>
                </span>
                <span style="float:right">Huşgeldiniz <?=$_SESSION['loginName']?> , <a href="index.php">Çıkış</a></span>
            </div>
        </td>
    </tr>
    <tr>
        <td id="main">
            <input type="text" id="baslik" />
            <input type="text" id="gbaslik" style="float:left"/>
            <input type="text" id="modules" style="float:left"/>
            <select id="plang" >
              <option value ="TR">Türkçe</option>
              <option value ="EN">English</option>
            </select>
           <span id="toolbar"></span>
            <textarea id="editor"></textarea>
        </td>
        <td id="kutular">
            <div class="header"> Sayfalar </div>
            <span style="float:right"><a href="#" onClick="ShowPageList()">Yenile</a></span>
            <span id="pageList"></span>
        </td>
    </tr>
    <tr>
        <td id="icerik" colspan=2>
            <div id="ayrintilar">
            <?php
                $PP->ShowLogs();
            ?>
            </div>
        </td>
    </tr>
    </table>
    </center>
    </body>
    </html>

<?php

    }
    else
        header("location: index.php");
?>
