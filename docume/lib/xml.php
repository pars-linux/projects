<?php

    function get_xml($file){
        if (file_exists($file)) {
            $trans_xml = fopen( $file,"r");
            $xml_content = fread ( $trans_xml,filesize($file));
            return simplexml_load_string( $xml_content);
        }
        else
            return 0;
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
