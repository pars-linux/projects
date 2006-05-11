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

?>
