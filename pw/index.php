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
        }

        function showit(originalRequest){
            var node = originalRequest.responseXML;
            var root = node.getElementsByTagName('Page').item(0);
            var content = root.getElementsByTagName('content').item(0);
            var dblog = root.getElementsByTagName('dblog').item(0);
            /*
            var channel = node.getElementsByTagName('channel').item(0);
            var title = channel.getElementsByTagName('title').item(0).firstChild.data;
            var link = channel.getElementsByTagName('link').item(0).firstChild.data;
            $('editor').innerHTML = "";
            */
            $('editor').innerHTML = content.textContent;
            $('ayrintilar').innerHTML = dblog.textContent + $('ayrintilar').innerHTML;
            
        }

    </script>
    </head>

    <body>
    <center>

    <!-- Content -->

    <table>
    <tr>
        <td id="header">
            <div id="menu">  </div>
        </td>
    </tr>
    <tr>
        <td id="main">
            <textarea id="editor" width="100%" height="100%"></textarea>
        </td>
        <td id="kutular">
            <div class="header"> Sayfalar </div>
            <?php
                $PageList = PrettyList($PP->GetRecord($TableA,'*'));
                foreach ($PageList as $Key=>$Value) {
                    echo '<div class="';
                    echo (($Key+1)%2)? 'koyu' : 'acik';
                    echo '">';
                    echo ($Key+1).'::';
                    echo '<b>'.$Value['Parent'].'</b>::';
                    echo JsLink($Value['ID'],$Value['Title'],'Edit');
                    echo '</div>';
                }
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

