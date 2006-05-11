<?php

    /** Gökmen GÖKSEL, gokmen@pardus.org.tr **/

    setlocale(LC_TIME,"tr_TR.UTF8");

    /**
     * build_smarty
     *
     * @access public
     * @return void
     */
    function build_smarty(){
        global $smarty;
        require("lib/smarty/Smarty.class.php");
        $smarty = new Smarty;
        $smarty->template_dir   = "templates/";
        $smarty->plugins_dir    = array("lib/smarty/plugins");
        $smarty->cache_dir      = "cache";
        $smarty->caching        = "true";
        $smarty->compile_dir    = "lib/smarty/compile";
        $smarty->force_compile  = "1";
        $smarty->clear_all_cache();
    }

    /**
     * ssv
     *
     * @param mixed $varname
     * @param mixed $var
     * @access public
     * @return void
     */
    function ssv($varname, $var){
        global $smarty;
        $smarty->assign($varname,$var);
    }


    /**
     * build_defaults
     *
     * @param mixed $slide_header
     * @param mixed $slide_author
     * @param mixed $author_email
     * @param mixed $author_firm
     * @param string $slide_theme
     * @access public
     * @return void
     */
    function build_defaults($slide_header,$slide_author,$author_email,$author_firm,$slide_theme="default"){
        global $smarty;
        ssv("Header",$slide_header);
        ssv("Author",$slide_author);
        ssv("Email" ,$author_email);
        ssv("Firm"  ,$author_firm );
        $smarty->template_dir = $smarty->template_dir.$slide_theme."/";
        ssv("Temp"  ,$smarty->template_dir);
    }

    /**
     * get_xml
     *
     * @param mixed $file
     * @access public
     * @return void
     */
    function get_xml( $file){
        $xml_file = "presentations/".$file;
        $trans_xml = fopen( $xml_file,"r");
        $xml_content = fread ( $trans_xml,filesize($xml_file));
        return simplexml_load_string( $xml_content);
    }


    function xml2html($node){
        global $smarty;
        $node = preg_replace("#/- #is","<li>",$node);
        $node = preg_replace("#/-- #is","<li style=\"padding-left:30px;list-style: square inside;\">",$node);
        $node = preg_replace("#/--- #is","<li style=\"padding-left:60px;\">",$node);
        $node = preg_replace("#/line/ (.+?) //line/#is","<p> \\1 </p>",$node);
        $node = preg_replace("#/code/ (.+?) //code/#is","<pre> \\1 </pre>",$node);
        $node = preg_replace("#/br/#is","<br />",$node);
        $node = preg_replace("#/center/ (.+?) //center/#is","<center> \\1 </center>",$node);
        $node = preg_replace("#/vcenter/ (.+?) //vcenter/#is","<div class=\"vcenter\"> \\1 </div>",$node);
        $node = preg_replace("#/c:(.+?)/ (.+?) //c/#is","<span style=\"color:\\1\"> \\2 </span>",$node);
        $node = preg_replace("#/image/ (.+?) //image/#is","<div style=\"text-align:center;\"><img src=\"presentations/images/\\1\" alt=\"[image]\"></div>",$node);
        $node = preg_replace("#/image f:(.+?)/ (.+?) //image/#is",
                             "<div style=\"float:\\1\;\"><img src=\"presentations/images/\\2\" alt=\"[image]\"></div>",$node);
        return $node;
    }

    function get_node($xml,$node,$field){
        $i=0;
        foreach ($xml->page as $pages){
            if ($i==$node){
                switch($field) {
                    case "content":
                        return $pages->content;
                    break;
                    case "list":
                        return $pages->content->list;
                    break;
                    case "header":
                        return $pages->header;
                    break;
                }
            }
            else $i++;
        }
    }
?>
