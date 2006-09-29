<?php

    session_start();
    require_once ('../config.php');
    if (session_is_registered($SessionKeyword) AND $_SESSION['state']=="A") {

?>
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

        function Del(nid,title) {

        var agree=confirm("'"+title+"' başlıklı kayıt silinecek. \n Onaylıyor musunuz ?");
        if (agree){
            Element.show('over');
            ClearFields();
            var url ='request.php';
            var linke = 'Delete='+nid;
            //alert (linke);
            var AjaxPointer = new Ajax.Request(
                url,
                {
                  method:'post',
                  parameters: linke,
                  onComplete: CleanUp
                }
            );
        }
        else
            return;
        }

        function Save(nid){
            Element.show('over');
            var url ='request.php';
            var _content = encodeURIComponent($('editor').value);
            var linke = 'PageID='+nid+'&Title='+$('baslik').value+'&NiceTitle='+$('gbaslik').value+'&Modules='+$('modules').value+'&Plang='+$('plang').value+'&Content='+_content;
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
            $('gbaslik').value          = root.getElementsByTagName('ntitle').item(0).textContent;
            $('modules').value          = root.getElementsByTagName('modules').item(0).textContent;
            $('plang').selectedIndex    = root.getElementsByTagName('plang').item(0).textContent;

            pidp = root.getElementsByTagName('pidp').item(0).textContent;
            $('toolbar').innerHTML = "<a href=# onClick=\"Save('"+pidp+"');\">Kaydet</a>";

            ShowPageList();
        }

        function ClearFields(){
            $('editor').value = "";
            $('editor').innerHTML = $('editor').value;
            $('baslik').value = "";
            $('gbaslik').value = "";
            $('modules').value = "";
            $('toolbar').innerHTML ="";
            $('plang').selectedIndex = 0;
            $('ayrintilar').innerHTML = "";
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

        function CleanUp(req){
            ClearFields();
            ShowPageList();
            Element.hide('over');
            $('ayrintilar').innerHTML = req.responseText;
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

        function ToggleHTML() {
            if ($('htmleditor').style.display=='none') {
                $('htmleditor').innerHTML = $('editor').value;
                $('htmleditor').innerHTML = "<a href=# onClick=\"ToggleHTML();\">[x] Kapat</a><br>" + $('htmleditor').innerHTML;
                Element.show('htmleditor');
                Element.hide('editor')
            }
            else {
                Element.hide('htmleditor');
                Element.show('editor');
            }
        }

<?php } ?>
