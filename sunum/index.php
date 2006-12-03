<?php

    /** Gökmen GÖKSEL, gokmen@pardus.org.tr **/

    include 'tool.php';
    $dir = "./presentations/";

    if (isset($_GET['file'])) {
        $xml = get_xml($_GET['file']);

        if (isset($_GET['pagelist'])) {
            print get_page_list($xml,$_GET['file']);
            return;
        }

        if ($_GET["page"]<>"") $page=$_GET["page"]; else $page=0;

        build_smarty();
        build_defaults($xml->header,$xml->author,$xml->email,$xml->firm);

        if (count($xml->page)>$page+1)
            $right=$page+1;
        else
            $right=-1;
        if ($page>0)
            $left=$page-1;
        else
            $left =-1;

        ssv("File",$_GET['file']);
        ssv("RightNode",$right);
        ssv("LeftNode" ,$left );
        ssv("NextNode" ,get_node($xml,$page+1,"header"));
        ssv("PrevNode" ,get_node($xml,$page-1,"header"));
        ssv("PageHeader",xml2html(get_node($xml,$page,"header")));
        ssv("Content"  , xml2html(get_node($xml,$page,"content")));
        ssv("PageCount", $page." / ".(count($xml->page)-1));
        $smarty->display("page.html");

        return;
    }

    else
        show_file_list($dir);

?>
