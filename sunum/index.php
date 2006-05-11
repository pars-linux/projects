<?php
 
    /** Gökmen GÖKSEL, gokmen@pardus.org.tr **/

    include 'tool.php';

    $xml = get_xml( "sunum.xml");
    $page= $_GET["page"];
   
    build_smarty(); 
    build_defaults($xml->header,$xml->author,$xml->email,$xml->firm);
    //build page navigations ..
    if (count($xml->page)>$page) $right=$page+1; else $rigth=FALSE;
    if ($page>0)                 $left =$page-1; else $left =FALSE;
    

    ssv("RightNode",$right);
    ssv("LeftNode" ,$left );

    $smarty->display("page.html");
  
    //echo count( $xml->page);
    //foreach ($xml->page as $pages )
      //  echo $pages->content."<br>"."<b>".$right."</b><br>";

?>
