<?php

    include_once ("globals.php");

    set_smarty_vars("categories",get_categories());
    set_smarty_vars("old_entries",get_entries_by_month());

    /* ACTION - new-entry */
    if (isset($_GET["entry"])) {
        $_POST["state"]=="Yayınla" ? $_POST["state"]=1 : $_POST["state"]=0;
        if (isset($_GET["add"]) AND isset($_POST["date"]) AND isset($_POST["title"]) AND isset($_POST["entry"])):
            if ($eid=add_entry ($_SESSION["uid"],$_POST["title"],$_POST["entry"],$_POST["date"],$_POST["category"],$_POST["state"])) header ("location: ?entry&ok&node=".$eid);
            else set_smarty_vars("error",ERROR);
        elseif (isset($_GET["delete"]) AND isset($_GET["id"])):
            if (del_category ($_GET["id"])) header ("location: ?categories");
            else set_smarty_vars("error",ERROR);
        elseif (isset($_GET["update"]) AND isset($_POST["id"])):
            if ($eid=update_entry ($_POST["id"],$_POST["title"],$_POST["entry"],$_POST["date"],$_POST["category"],$_POST["state"])) header ("location: ?entry&node=".$eid);
            else set_smarty_vars("error",ERROR);
        elseif (isset($_GET["node"])):
            set_smarty_vars("entry",get_entry($_GET["node"]));
            set_smarty_vars("entry_categories",get_entry_categories($_GET["node"]));
        endif;
        $_GET["node"]<>"" ? $smarty->display("edit-entry.html") : $smarty->display("new-entry.html");
    }
    /* END ACTION - new-entry */

    elseif (isset($_GET["olds"])) {
        set_smarty_vars("entry",get_entries($_SESSION["uid"]));
        $smarty->display("old-entries.html");
    }
    /* ACTION - categories */
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
    /* END ACTION - categories */

    /* ACTION - dashboard */
    else {
        $smarty->display("dashboard.html");
    }
    /* END ACTION - dashboard */
?>
