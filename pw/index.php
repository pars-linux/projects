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
            Element.show('over');
            var url ='request.php';
            var linke = 'PageID='+nid;
            var AjaxPointer = new Ajax.Request(
                url,
                {
                  method:'get',
                  parameters: linke,
                  onComplete: showXML
                }
            );
        }

        function Save(nid){
            Element.show('over');
            var url ='request.php';
            var _content = encodeURIComponent($F('editor'));
            var linke = 'PageID='+nid+'&Title='+$('baslik').value+'&Parent='+$F('parent')+'&Ptype='+$F('ptype')+'&Content='+_content;
            //alert (linke);
            var AjaxPointer = new Ajax.Request(
                url,
                {
                  method:'post',
                  postBody: linke,
                  onComplete: showXML
                }
            );
        }

        function showXML(originalRequest){
            Element.hide('over');
            var node = originalRequest.responseXML;
            var root = node.getElementsByTagName('Page').item(0);
            $('editor').value           = root.getElementsByTagName('content').item(0).textContent;
            $('editor').innerHTML       = $('editor').value;
            $('ayrintilar').innerHTML   = root.getElementsByTagName('dblog').item(0).textContent;
            $('baslik').value           = root.getElementsByTagName('title').item(0).textContent;
            $('parent').selectedIndex   = root.getElementsByTagName('parent').item(0).textContent;
            $('ptype').selectedIndex    = root.getElementsByTagName('ptype').item(0).textContent;
            pidp = root.getElementsByTagName('pidp').item(0).textContent;
            $('toolbar').innerHTML = "<a href=# onClick=\"Save('"+pidp+"');\">Kaydet</a>";

            ShowPageList();
        }

        function ClearFields(){
            $('editor').value = "";
            $('editor').innerHTML = $('editor').value;
            $('baslik').value = "";
            $('toolbar').innerHTML ="";
        }

        function ShowPageList(){
            var ajax = new Ajax.Updater(
                'pageList',
                'request.php?PageList',
                {
                    method:'get',
                    onComplete: showPlain
                }
            );
        }

        function showPlain(req)
        {
            $('pageList').innerHTML = req.responseText;
        }

        function AddNewPage(){
            ClearFields();
            $('toolbar').innerHTML = "<a href=# onClick=\"Save('0');\">Ekle</a>";
            $('toolbar').innerHTML = $('toolbar').innerHTML + "<a href=# onClick=\"ClearFields();\">İptal</a>";
        }

    </script>
    </head>

    <body onLoad="ClearFields();ShowPageList();">

    <div id="over" style="display:none">
        <div style="padding-top:25%;color:#FFF;">
            <img src="images/spin.gif"/>
            <br>çalışıyor
        </div>
    </div>

    <center>

    <!-- Content -->

    <table style="height:100%;">
    <tr>
        <td id="header">
            <div id="menu">
                <a href="#" onClick="AddNewPage()">Yeni Ekle</a>
            </div>
        </td>
    </tr>
    <tr>
        <td id="main">
            <input type="text" id="baslik" />
            <select id="parent" >
              <option value ="B">Bireysel</option>
              <option value ="K">Kurumsal</option>
              <option value ="G">Geliştirici</option>
            </select>
             <select id="ptype" >
              <option value ="P">Sayfa</option>
              <option value ="D">Döküman</option>
            </select>
            <span id="toolbar"></span>
            <textarea id="editor"></textarea>
        </td>
        <td id="kutular">
            <div class="header"> Sayfalar <span style="float:right"><a href="#" onClick="ShowPageList()">Yenile</a></div>
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

