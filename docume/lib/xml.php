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

    function set_($xml,$table,$field,$value){
        $k=$j=0;
        foreach ($xml->table as $tables){
            if ($table==$tables['name']){
                foreach ($tables->field as $fields){
                    if ($fields['name']==$field)
                        $xml->table[$k]->field[$j]=$value;
                    else
                        $j++;
                }
            } else $k++;
        }
        return $xml;
    }

?>
