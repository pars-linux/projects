<?php

    class MakeForms {

        public $vezir;
        public $xml;

        function MakeForms($xml,$Vezir=false){
            $this->xml = $xml;
            if (false !== $Vezir)
                $this->vezir=$Vezir;
        }

        function Build($xml,$show,$method="GET") {
            foreach ($xml->table as $tables){
                $show=="all"?$que="all":$que=$tables['name'];
                if ($show==$que){
                $ret.= "<h3>".$xml->name." :: ".$tables['name']." table </h3>\n";
                $ret.= "<form action='?' method='$method' id='".$tables['name']."' class='cssform'>\n";
                foreach ($tables->field as $fields){
                    $ret.="<p><label for='{$fields['name']}'>{$fields['name']}</label>\n";
                    switch ($fields["type"]) {
                        case "text":
                            $ret.="<textarea id='{$fields['name']}' rows='5' cols='35'>{$fields}</textarea>\n";
                        break;
                        case "char":
                            $ret.="<input type='text' id='{$fields['name']}' value='{$fields}'/>\n";
                        break;
                        case "set":
                            $values=explode(",",$fields['values']);
                            foreach ($values as $value) {
                                $fields==$value ? $cc="CHECKED":$cc="";
                                $ret.="{$value} <input type='radio' name='{$fields['name']}' value='{$value}' $cc />";
                            }
                            $ret.="<br />\n";
                        break;
                    }
                    $ret.="</p>\n";
                }
                $ret.="<p><label>Submit</label>
                        <input type='submit' value='Submit' />\n
                        <input type='reset' value='Reset' />\n
                       </p></form>";
                }
            }
            return $ret;
        }

        function ParseForms($show="all"){
            echo $this->Build($this->xml,$show);
        }
    }

?>
