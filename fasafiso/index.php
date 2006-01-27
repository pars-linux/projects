<?php
include_once("globals.php");

// set pagination numbers
if($_GET['start']){$start = $_GET['start']; $end = ($_GET['start']+$config['core']['postperpage']);}
else{$start = '0'; $end = $config['core']['postperpage'];}

if(empty($id) OR $id = ""){$id = "";}
if(isset($_GET['id'])){$id = $_GET['id'];}

db_connection('connect', $config['db']['hostname'].':'.$config['db']['port'], $config['db']['username'], $config['db']['password'], $config['db']['databasename'], $config['db']['connectiontype']);

        if (isset($_GET["date"]) OR isset($_GET["cat"])) $end=99999999; //Yok artık
	$posts = get_posts($id,"{$_GET['cat']}","{$_GET['date']}","{$_GET['author']}","1",$start,$end);
	set_smarty_vars("posts",$posts);
	$archives = get_archives();
	set_smarty_vars("archives",$archives);
	$categories = get_categories();
	set_smarty_vars("categories",$categories);
        $links = get_links();
        set_smarty_vars("links", $links);

	if($id){
		if ($_GET["action"]=="addcomment"){ if (add_comment($id,$_POST["author"],$_POST["email"],$_POST["website"],$_POST["comment"],$_POST["date"])) header ("location: ?id=".$id."#comments");}
		$comments = get_comments("",$id,"1");
		set_smarty_vars("comments",$comments);
		$smarty->display("post.html");
	}
	else{
		$smarty->display("posts.html");
	}

db_connection("disconnect");
?>