<?php

    include_once ("globals.php");

    set_smarty_vars("categories",get_categories());

    if (isset($_GET["new-entry"])) {
        $smarty->display("new-entry.html");
    }

    elseif (isset($_GET["categories"])) {
        if (isset($_GET["edit"]) AND isset($_GET["id"])) set_smarty_vars ("editid",$_GET["id"]);
        if (isset($_GET["add"])  AND isset($_POST["category"])):
            if (add_category ($_POST["category"],$_POST["nicename"],$_POST["description"])) header ("location: ?categories");
            else set_smarty_vars("error",ERROR);
        elseif (isset($_GET["delete"]) AND isset($_GET["id"])):
            if (del_category ($_GET["id"])) header ("location: ?categories");
            else set_smarty_vars("error",ERROR);
        elseif (isset($_GET["update"]) AND isset($_POST["category"])):
            if (update_category ($_POST["id"],$_POST["category"],$_POST["nicename"],$_POST["description"])) header ("location: ?categories");
            else set_smarty_vars("error",ERROR);
        endif;
        $smarty->display("categories.html");
    }

    else {
        $smarty->display("dashboard.html");
    }

?>