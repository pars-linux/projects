<?php
    
    require_once ('config.php');
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
    <script>
        function Edit(nid) {
            var url ='request.php';
            var linke = 'PageID='+nid;
            var AjaxPointer = new Ajax.Request(
                url,
                { 
                  method:'get', 
                  parameters: linke,
                  onComplete: showit
                }
            );
            $('toolbar').innerHTML = "<a href=# onClick=\"Save('"+nid+"');\">Kaydet</a>";
        }

        function Save(nid){
            var url ='request.php';
            var linke = 'PageID='+nid+"&Title="+$('baslik').innerHTML+"&Content="+$('editor').value;
            alert (linke); 
            var AjaxPointer = new Ajax.Request(
                url,
                { 
                  method:'post', 
                  parameters: linke,
                  onComplete: showit
                }
            );
        }

        function showit(originalRequest){
            var node = originalRequest.responseXML;
            var root = node.getElementsByTagName('Page').item(0);
            $('editor').reset;
            $('editor').innerHTML       = root.getElementsByTagName('content').item(0).textContent;
            $('ayrintilar').innerHTML   = root.getElementsByTagName('dblog').item(0).textContent;
            $('baslik').innerHTML       = root.getElementsByTagName('title').item(0).textContent;
            $('type').innerHTML         = root.getElementsByTagName('type').item(0).textContent;
        }

    </script>
    </head>

    <body>
    <center>

    <!-- Content -->

    <table style="height:100%;">
    <tr>
        <td id="header">
            <div id="menu">  </div>
        </td>
    </tr>
    <tr>
        <td id="main">
            <span id="baslik"></span>
            <span id="toolbar">
            </span>
            <textarea id="editor"></textarea>
        </td>
        <td id="kutular">
            <div class="header"> Sayfalar </div>
            <?php
                PageList(PrettyList($PP->GetRecord($TableA,'*')));
            ?>
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

