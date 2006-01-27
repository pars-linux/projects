<?php
include_once("config.php");
include_once("version.php");

// including smarty class
include_once($config['core']['path'].$config['smarty']['libdir']."/Smarty.class.php");

// configuring smarty
$smarty = new Smarty;
if(isset($_GET['tema'])){$config['core']['theme']=$_GET['tema'];}
$smarty->template_dir = $config['core']['path'].$config['smarty']['tpldir']."/".$config['core']['theme'];
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
$smarty->assign("blogurl", $config['core']['webaddress']);
$smarty->assign("themepath", $config['smarty']['tpldir']."/".$config['core']['theme']);

// including fasafiso functions
include_once("functions.php");

setlocale(LC_TIME,"tr_TR.UTF8");
?>