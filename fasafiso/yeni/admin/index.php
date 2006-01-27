<?php

	include_once("../globals.php");
        include("functionss.php");
	require ("session.php");
	if (session_is_registered("fasafiso")){
		if (isset($_POST["publish"])) 	$state="1";
		if (isset($_POST["save"])) 	$state="0";
		switch ($_GET["act"]){
			case "add":
				if ($tmp_id=add_entry($_SESSION["uid"],$_POST["category"],$_POST["title"],$_POST["text"],$_POST["date"],"add",$state))
				header ("location: ?act=new&id=".$tmp_id."&ok");
				else echo "Sistem Hatası !!";
			break;
			case "update":
				if (add_entry($_SESSION["uid"],$_POST["category"],$_POST["title"],$_POST["text"],"","update",$state,$_POST["id"])) header ("location: ?act=edit&id=".$_POST["id"]."&ok");
				else echo "Sistem Hatası !!";
			break;
			case "del":
				if (del_entry($_SESSION["uid"],$_GET["id"])) header ("location: ?act=old&date=".$_GET['date']);
				else echo "Kayıt mevcut değil ya da bir Sistem Hatası meydana geldi !!";
			break;
			case "cat":
				switch ($_GET["x"]){
					case "add":
					if (add_cat($_POST["category"],$_POST["description"])) header ("location: ?act=cat");
					else echo "Hata kategori eklenmedi !!";
					break;
					case "del":
					if (del_cat($_GET["id"])) header ("location: ?act=cat");
					else echo "Hata kategori silinmedi !!";
					break;
					case "upd":
					if (add_cat($_POST["category"],$_POST["description"],"update",$_POST["id"])) header ("location: ?act=cat");
					else echo "Hata kategori güncellenemedi !!";
					break;
				}
			break;
			case "com":
				switch ($_GET["x"]){
					case "chs":
					if (ed_comment($_GET["id"],$_GET["v"])) header ("location: ?act=com&eid=".$_GET["eid"]."&date=".$_GET["date"]);
					else echo "Hata yorum durumu güncellenemedi !!";
					break;
					case "del":
					if (ed_comment($_GET["id"])) header ("location: ?act=com&eid=".$_GET["eid"]."&date=".$_GET["date"]);
					else echo "Hata yorum silinmedi !!";
					break;
				}
			break;
			case "users":
				switch ($_GET["x"]){
					case "add":
					if (add_user($_POST["name"],$_POST["uname"],$_POST["email"],$_POST["password"])) header ("location: ?act=users");
					else echo "Hata kullanıcı eklenmedi !!";
					break;
					case "del":
					if (del_user($_GET["id"])) header ("location: ?act=users");
					else echo "Hata kullanıcı silinmedi !!";
					break;
					case "upd":
					if (add_user($_POST["name"],$_POST["uname"],$_POST["email"],$_POST["password"],"update",$_POST["id"])) header ("location: ?act=users");
					else echo "Hata kullanıcı bilgileri güncellenemedi !!";
					break;
				}
			break;
		}
	if (isset($_GET["ok"])){
// 		$results=get_posts(mysql_insert_id());
		$package=get_posts($_GET["id"]);
		$warn="<span class=\"saved\"><img src=\"images/warn.png\">\" <b>".$package[0]["title"]."</b> \" başlıklı kayıt günlüğe eklendi.Bu kayıdı <a href=\"?act=edit&id=".$package[0]["id"]."\">buradan</a> düzenleyebilirsiniz.</span><br><br>";
		$warn2="<span class=\"saved\"><img src=\"images/warn.png\">\" <b>".$package[0]["title"]."</b> \" başlıklı kayıt güncellendi..</span><br><br>";
		}
	}
?>

<html>
	<head>
		<title>FasaFiso</title>
		<script src="../3rdparty/editor/whizzywig.js" type="text/javascript"></script>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link rel="stylesheet" type="text/css" href="style.css">
		<script LANGUAGE="javascript">
		
			function confirmSubmit(){
				var agree=confirm("Onaylıyor musunuz ?");
				if (agree) return true;
				else return false ;
			}

		</script>
		<script type="text/javascript">

			function toggleVisibility(el, src) {
				var v = el.style.display == "block";
				var str = src.innerHTML;
				el.style.display = v ? "none" : "block";
				src.innerHTML = v ? str.replace(/up/, "down") : str.replace(/down/, "up");
			}
			
		</script>
	</head>
	<body>
<?
	if (session_is_registered("fasafiso")){
	//<a href="#" onclick="toggleVisibility(document.getElementById('menu2'), this); return false"><img src="images/old.png">Eski Yazılar <img src="images/down.png"></a><br>
		?>
		<center>
		<div class="bar"><img src="images/bar.png"></div>
		<div class="main">
		<div class="menu">
			<div class="menu_h"><a href="#" onclick="toggleVisibility(document.getElementById('menu'), this); return false">MENU</a></div>
			<p id="menu">
			<a href="?act=new"><img src="images/new.png">Yeni Yazı Ekle</a><br>
			<a href="#" onclick="toggleVisibility(document.getElementById('menu2'), this); return false"><img src="images/old.png">Eski Yazılar</a><br>
			<a href="#" onclick="toggleVisibility(document.getElementById('menu3'), this); return false"><img src="images/com.png">Yorumlar</a><br>
			<? if ($_SESSION["uid"]==1) { ?>
			<a href="?act=cat"><img src="images/category.png">Kategoriler</a><br>
			<a href="?act=users"><img src="images/users.png">Kullanıcılar</a><br>
			<? } ?> 
			<a href="?quit"><img src="images/quit.png">Çıkış</a>
			</p>
		</div>
		<div class="content">
		
		<?
		switch ($_GET["act"]){
			case "new":
				echo "<div class=\"header\">Yeni bir girdi ekleyin ..".$warn."</div><br>";
				editor();
			break;
			case "edit":
				echo "<div class=\"header\">Girdileri düzenleyin ..".$warn2."</div><br>";
				editor($_GET["id"]);
			break;
			case "old":
				get_post_lists($_GET["date"],"{$_SESSION["uid"]}");
			break;
			case "cat":
				if ($_SESSION["uid"]=="1") get_categoriess(1,$_GET["id"]);
				else echo "Üzgünüm, Bu işlem için yetkiniz yok !!";
			break;
			case "users":
				if ($_SESSION["uid"]=="1") get_users($_GET["id"]);
				else echo "Üzgünüm, Bu işlem için yetkiniz yok !!";
			break;
			case "com":
				get_post_lists($_GET["date"],"{$_SESSION["uid"]}",1,$_GET["id"],$_GET["eid"]);
			break;
			default:
			echo "Hoşgeldiniz ".$_SESSION["user"];;
		}
		?>
		
		</div>
		<div class="smenu" id="menu2" style="display:none;">
			<p class="rayt"><a href="#" onclick="toggleVisibility(document.getElementById('menu2'), this); return false">Eski Yazılar ..<img src="images/close.png"></a></p>
		<?
		$archives = get_archives($_SESSION["uid"]);
		for ($i=0; $i<count($archives); $i++){
			echo "<a href=\"?act=old&date=".$archives[$i][date]."\">".$archives[$i][name]." (".$archives[$i][count].")"."</a><br>";
		}
		?>
		</div>
		<div class="smenu" id="menu3" style="display:none;">
			<p class="rayt"><a href="#" onclick="toggleVisibility(document.getElementById('menu3'), this); return false">Yorumlar ..<img src="images/close.png"></a></p>
		<?
		$archives = get_archives($_SESSION["uid"]);
		for ($i=0; $i<count($archives); $i++){
			echo "<a href=\"?act=com&date=".$archives[$i][date]."\">".$archives[$i][name]." (".$archives[$i][count].")"."</a><br>";
		}
		?>
		</div>
		</div>
		</center>
		<?
	}
	
	else { 
		login_form($error); 
	}
?>
	<a id="toocool" href="http://www.w3junkies.com/toocool/">No EKSPLORER !!</a>
	</body>
</html>
