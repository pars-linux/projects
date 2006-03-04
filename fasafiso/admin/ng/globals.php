<?php
// including common libraries
include_once("../../config.php");
include_once("../../version.php");

// including utils alla about administration
include_once("utils.php");

// including smarty class
include_once($config['core']['path'].$config['smarty']['libdir']."/Smarty.class.php");

// configuring smarty
$smarty = new Smarty;
$smarty->template_dir = $config['core']['path']."admin/ng/template";
$smarty->plugins_dir = array($config['core']['path'].$config['smarty']['libdir']."/plugins");
$smarty->cache_dir = $config['core']['path'].$config['smarty']['cachedir'];
$smarty->caching = $config['smarty']['caching'];
$smarty->compile_dir = $config['core']['path'].$config['smarty']['compiledir'];
$smarty->force_compile = $config['smarty']['forcecompile'];
$smarty->clear_all_cache();

// preparing smarty
$smarty->assign("fasafiso_signature","<a href=\"http://fasafiso.org/\" title=\"FasaFiso v{$config['fasafiso']['version']} (r{$config['fasafiso']['build']})\">FasaFiso v{$config['fasafiso']['version']}</a>");
$smarty->assign("fasafiso_signature_text","FasaFiso v{$config['fasafiso']['version']} ({$config['fasafiso']['builddate']})");
$smarty->assign("blogname", $config['core']['blogname']);
$smarty->assign("blogdesc", $config['core']['blogdesc']);
$smarty->assign("blogurl", $config['core']['webaddress']."admin/ng/template/");
$smarty->assign("themepath", "template");

//connection to the database
db_connection('connect', $config['db']['hostname'].':'.$config['db']['port'], $config['db']['username'], $config['db']['password'], $config['db']['databasename'], $config['db']['connectiontype']);

setlocale(LC_TIME,"tr_TR.UTF8");

// session_start
session_start();

// user check and register session
if (isset($_GET["do_login"])){
	$username = rtag($_POST['username']);
	$password = rtag($_POST['password']);
	if ($ird=get_user_details($username,$password)){
		session_unregister("fasafisong");
		session_register("fasafisong");
		$_SESSION["uid"]=$ird[0]['id'];
		$_SESSION["uname"]=$ird[0]['name'];
		$_SESSION["user"]=$username;
		$_SESSION["state"]=$ird[0]['state'];
		header ("location: ?entry");
	}
	else $wrong_pass=TRUE;
}
elseif (isset($_GET["quit"])) { session_unregister("fasafisong"); header ("location: "); }
if (!session_is_registered("fasafisong")){ $smarty->display("login.html"); die(); }

?>