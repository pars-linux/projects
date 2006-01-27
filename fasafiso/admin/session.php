<?php

	session_start();
	if (isset($_GET['quit'])) { session_unregister("fasafiso"); header ("location: index.php"); }
	db_connection('connect', $config['db']['hostname'].':'.$config['db']['port'], $config['db']['username'], $config['db']['password'], $config['db']['databasename'], $config['db']['connectiontype']);
	if (isset($_POST["username"])){
		if ($ird=check_permit($_POST["username"],$_POST["password"])){
		session_unregister("fasafiso"); @session_register("fasafiso"); $_SESSION["uid"]=$ird;$_SESSION["user"]=$_POST["username"]; header ("location: index.php");
		}
		else $error="
				<tr> 
            		<td class=\"warn\"> Kullanıcı Adı ya da Parola Hatalı !!</td>
          		</tr> ";
	}

?>