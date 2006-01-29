<?php

    include_once ("globals.php");

    set_smarty_vars("categories",get_categories());

    if (isset($_GET["new-entry"])) {
        $smarty->display("new-entry.html");
    }

    elseif (isset($_GET["categories"])) {
        $smarty->display("categories.html");
    }

    else {
        $smarty->display("dashboard.html");
    }

?>