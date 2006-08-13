<?php

    #I used Textile for text manipulating.
    require_once ('Textile.php');

    function ParseComments($Vezir,$ID){
        echo $ID;
    }

    function ParseAuthor($Vezir,$ID) {
        $Raw = $Vezir->GetRecord("Users","*",$ID);
        if ($Raw)
            echo $Raw[0]['RealName'];
        else
            echo "Unkown User";
    }

    function ParseContent($Content) {
        $Textile = new Textile;
        echo $Textile->process($Content);
    }
?>
