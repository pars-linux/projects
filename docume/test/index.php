<!DOCTYPE html
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="tr" xml:lang="tr">
<head>
    <title>Docume</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="style.css" rel="stylesheet" type="text/css" />
</head>
<body>

<?php

    #require_once ("../lib/vezir.php");
    #$_db = new Vezir();

    $db_dir = "../_db/";

    if (isset($_GET["file"])) {
        $file_ = $db_dir.$_GET["file"];
        if (file_exists($file_)){
            require_once ("../lib/xml.php");
            require_once ("../lib/xhtml.php");

            $xml=get_xml($file_);

            $xhtml = new MakeForms($xml);
            $xhtml->ParseForms();

            return;
        }
    }

    # file list..
    if ($handle = opendir("../_db/"))
        while (false !== ($file=readdir($handle)))
        if ($file<>"." and $file<>"..")
            echo "<a href='{$PHP_SELF}?file=$file'>$file</a><br/> ";
        else
            echo "$file<br/>";
?>

</body>
</html>
