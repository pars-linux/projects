<?php
# Just for administration pages ..

/**/	function editor($id=""){
		global $config;
		$st="add";
		if ($id<>""){
			$post=get_posts($id,"","",$_SESSION['uid']);
			$date=$post[0][date];
			$st="update";
			if ($post[0][status]) $durum="- Yazı yayında .."; else $durum="- Yazı geçici olarak kaydedilmiş .. Sayfada gözükmez !!";
		}
		else $date=date('YmdHi');
		?>

		<form action="?act=<?=$st?>" method="post" onsubmit="syncTextarea();">
			<p class="sari">Başlık : <input type="text" name="title" size="60" value="<?=$post[0]["title"]?>"><i><?=$durum?></i></p>
			<br>
			<textarea name="text" style="width:99%; height:280px" id="richtext"><?=$post[0]["text"]?></textarea>
			<script type="text/javascript">makeWhizzyWig("richtext", "all");</script>
			<input type="hidden" name="date" value="<?=$date?>">
			<input type="hidden" name="id" value="<?=$post[0]["id"]?>">
			<p class="sari">Kategori : 
		<?
			$archives=get_categories();
			$checked =get_cat($id,1);
			for ($i=0; $i<count($archives); $i++){
			if ($checked) foreach ($checked as $chok) if ($chok==$archives[$i][id]) $selected="CHECKED"; 
			echo "<input class=\"check\" ".$selected." type=\"checkbox\" value=\"".$archives[$i][id]."\" name=\"category[]\">".$archives[$i][name];
			$selected="";
			}
		?>	</p><br>

			<div class="right"><input class="buton" type="submit" name="publish" value="Yayınla"><input class="buton"  type="submit" name="save" value="Kaydet"></div>
		</form>
		<? if ($id) { ?>
		<p><a href="#" onclick="toggleVisibility(document.getElementById('details'), this); return false">Ayrıntılar <img src="images/down.png"></a></p>
		<p id="details" style="display: none;"><?
		echo "Yazar :".get_author_name($_SESSION["uid"])." , Tarih : ".$date['day']."-".$date['month']."-".$date["year"]." @ ".$date['hour'].":".$date["minute"]."</p>";
		}
	}

/**/	function act_cat($cat_id,$entry_id,$opt=""){
		global $config;
		$sql_word = "DELETE FROM {$config['db']['tableprefix']}category_act WHERE entry_id='{$entry_id}'";
		$sql_query = @mysql_query($sql_word);
		if ($cat_id) {
		foreach ($cat_id as $cat) {
			$sql_word = "INSERT INTO {$config['db']['tableprefix']}category_act VALUES ('', '{$cat}', '{$entry_id}')";
			$sql_query = @mysql_query($sql_word);
		}
		}	
	}

/**/	function ed_comment($id,$v=""){
		global $config;
		if ($v<>"") $sql_word ="UPDATE {$config['db']['tableprefix']}comments SET status='{$v}' WHERE id='$id'";
		else 	$sql_word ="DELETE FROM {$config['db']['tableprefix']}comments WHERE id='{$id}'";
		$sql_query = @mysql_query($sql_word);
		if($sql_query){$return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}

	
/**/	function login_form($error=""){
		?>
		<p>&nbsp;</p>
		<table class="login" align="center">
  		<tr>
    		<td><div align="center"> 
        		<table class="form_login">
          		<tr> 
            		<td height="172"> <div align="center"><img src="images/logo.png"></div></td>
          		</tr>
			<?=$error?>
			<form action="" method="post">
          		<tr> 
            		<td height="40"><div align="right">Kullanıcı Adı :
                		<input class="username" type="text" size="25" name="username">
              		</div></td>
          		</tr>
          		<tr> 
            		<td height="40"> <div align="right">Parola : 
                		<input class="password" type="password" size="25" name="password">
              		</div></td>
          		</tr>
          		<tr> 
            		<td height="40"> <div align="right"> 
                		<input type="submit" name="Submit" value="Giriş">
              		</div></td>
          		</tr>
			</form>
        		</table>
      		</div>
  		</tr>
		</table>
		<?php
	}

/**/	function get_post_lists($date="",$author="",$act=0,$id="",$eid=""){
		$archives=get_posts("","",$date,$author);
		$categories=get_categoriess();
		$getdate=conv_time("db2archive", $date);
		if (!$act) {
			echo "<div class=\"header\">".$getdate." kayıtlı yazılarınız ..</div><br>";
			?>
			<table class="post" border="0" height="96" width="100%">
				<tbody class="posts">
					<tr><th width="60%"><img src="images/m_down.png">Başlık</th><th width="7%" align="center">Tarih</th><th width="23%" align="center">Kategori(ler)</th><th width="7%" align="center">Düzenle</th><th width="4%" align="center">Sil</th></tr>
			<?
			for ($i=0; $i<count($archives); $i++){
				echo "<tr><td><a href=\"#\" onclick=\"toggleVisibility(document.getElementById('".$archives[$i][id]."'), this); return false\"><img src=\"images/down.png\">".$archives[$i][title]."</a><span id=\"".$archives[$i][id]."\" style=\"display: none;\">".$archives[$i]['entry']."</span></td><td align=\"center\">".$archives[$i][date][day]."/".$archives[$i][date][month]."/".$archives[$i][date][year]."</td><td align=\"center\">";
				if ($act_cat=get_cat($archives[$i][id],1)) foreach ($act_cat as $cat_act) echo get_category_name($cat_act).". ";
				echo "</td><td><center><a href=\"?act=edit&id=".$archives[$i][id]."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=del&id=".$archives[$i][id]."&date=".$date."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
			}
		}
		else {
			echo "<div class=\"header\">".$getdate." kayıtlı yazılarınıza ait yorumlar ..</div><br>";
			?>
			<table class="post" border="0" height="96" width="100%">
				<tbody class="posts">
					<tr><th width="68%"><img src="images/m_down.png">Başlık</th><th width="3%" align="center">YA</th><th width="7%" align="center">Tarih</th><th width="23%" align="center">Kategori(ler)</th></tr>
			<?
			for ($i=0; $i<count($archives); $i++){
				if ($eid<>$archives[$i][id]) $st="none"; else $st="block";
				echo "<tr><td><a href=\"#\" onclick=\"toggleVisibility(document.getElementById('".$archives[$i][id]."'), this); return false\"><img src=\"images/down.png\">".$archives[$i][title]."</a>
				<span id=\"".$archives[$i][id]."\" style=\"display:".$st.";\">";
				
				$ii=0;
				if ($comments = get_comments($id,$archives[$i][id],"")) {
				?>
				<table class="post" border="0" height="96" width="100%">
						<tbody class="posts">
						<tr><th width="25%">Gönderen</th><th width="60%">Yorum</th><th width="10%" align="center">Gözükür</th><th width="4%" align="center">Sil</th></tr>
				<?
					for ($ii=0; $ii<count($comments); $ii++){
						echo "<tr><td>"
						.$comments[$ii][author]
						."</td><td>"
						.$comments[$ii][comment]
						."</td><td>";
						if ($comments[$ii][status]) {$v=0;$img="true.png";} else {$v=1;$img="false.png";}
						echo "<a href=\"?act=com&date=".$date."&x=chs&v=".$v."&id=".$comments[$ii][id]."&eid=".$archives[$i][id]."\"><center><img src=\"images/".$img."\"></center></a></td>"
						."<td><center><a href=\"?act=com&date=".$date."&x=del&eid=".$archives[$i][id]."&id="
						.$comments[$ii][id]
						."\" onClick=\"return confirmSubmit()\">"
						."<img src=\"images/delete.png\"></a></center>"
						."</td></tr>";
					}
				?></tbody></table><?
				}
				
				echo "</span></td><td align=\"center\">".$ii."</td>
				<td align=\"center\">".$archives[$i][date][day]."/".$archives[$i][date][month]."/".$archives[$i][date][year]."</td><td align=\"center\">";
				if ($act_cat=get_cat($archives[$i][id],1)) foreach ($act_cat as $cat_act) echo get_category_name($cat_act).". ";
				//echo "</td><td><center><a href=\"?act=edit&id=".$archives[$i][id]."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=del&id=".$archives[$i][id]."&date=".$date."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
				echo "</td>";
			}
		}
		?>
			</tbody>
		</table>
		<?
	}

/**/	function get_categoriess($list=0,$id=""){
		global $config;

		$sql_word = "SELECT * FROM {$config['db']['tableprefix']}category";
		$sql_query = @mysql_query($sql_word);
		
		for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
				$assoc_arr = mysql_fetch_assoc($sql_query);
				$return_array[$i] = $assoc_arr;
				$sql_word_fsfs = "SELECT id FROM {$config['db']['tableprefix']}category_act WHERE cat_id='{$assoc_arr['id']}'";
				$sql_query_fsfs = @mysql_query($sql_word_fsfs);
				$number = @mysql_num_rows($sql_query_fsfs);
				$return_array[$i]['count'] = $number;
				// there is a bug in counting but itsn't important
				// now it shows draft or published writes count
		}
		
		if ($list) {
				?>
				<div class="header">Kategorileri düzenleyin ..</div><br>
				<table class="post" border="0" height="96" width="100%">
					<tbody class="posts">
						<tr><th width="7%">ID</th><th width="32%">Kategori</th><th width="45%">Açıklama</th><th width="8%" align="center">Düzenle</th><th width="8%" align="center">Sil</th></tr>
				<?
				for ($i=0; $i<count($return_array); $i++){
					if ($id==$return_array[$i]['id']){
					echo "<form method=\"POST\" action=\"?act=cat&x=upd\">
						<input type=\"hidden\" name=\"id\" value=\"".$return_array[$i]['id']."\">
					      <tr>
						<td>".$return_array[$i]['id']."</td>
						<td><input type=\"text\" name=\"category\" size=\"30\" value=\"".$return_array[$i]['name']."\"></td>
						<td><input type=\"text\" name=\"description\" size=\"50\" value=\"".$return_array[$i]['description']."\"></td>
						<td><center><input type=\"submit\" value=\"Güncelle\"></center></td><td><center><a href=\"?act=cat&x=del&id=".$return_array[$i]['id']."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
					}
					else {
					echo "<tr>
						<td>".$return_array[$i]['id']."</td>
						<td>".$return_array[$i]['name']."</td>
						<td>".$return_array[$i]['description']."</td>
						<td><center><a href=\"?act=cat&id=".$return_array[$i]['id']."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=cat&x=del&id=".$return_array[$i]['id']."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
					}
				}
				if (!$id) {
				?>
				<form method="POST" action="?act=cat&x=add">
				<tr><TD>Yeni :</TD><td><input type="text" name="category" size="30"></td><td><input type="text" name="description" size="50"></td><td colspan="2"><center><input type="submit" value="Ekle"></center></td></tr></form>
				<?
				}
				echo "</tbody></table>";
		}
		return $return_array;
	}

/**/	function get_post_list($date="",$author="",$act=0,$id="",$eid=""){
		$archives=get_posts("","",$date,$author);
		$categories=get_categories();
		$getdate=conv_time("db2archive", $date);
		if (!$act) {
			echo "<div class=\"header\">".$getdate." kayıtlı yazılarınız ..</div><br>";
			?>
			<table class="post" border="0" height="96" width="100%">
				<tbody class="posts">
					<tr><th width="60%"><img src="images/m_down.png">Başlık</th><th width="7%" align="center">Tarih</th><th width="23%" align="center">Kategori(ler)</th><th width="7%" align="center">Düzenle</th><th width="4%" align="center">Sil</th></tr>
			<?
			for ($i=0; $i<count($archives); $i++){
				echo "<tr><td><a href=\"#\" onclick=\"toggleVisibility(document.getElementById('".$archives[$i][id]."'), this); return false\"><img src=\"images/down.png\">".$archives[$i][title]."</a><span id=\"".$archives[$i][id]."\" style=\"display: none;\">".$archives[$i][text]."</span></td><td align=\"center\">".$archives[$i][date][day]."/".$archives[$i][date][month]."/".$archives[$i][date][year]."</td><td align=\"center\">";
				if ($act_cat=get_cat($archives[$i][id],1)) foreach ($act_cat as $cat_act) echo get_category_name($cat_act).". ";
				echo "</td><td><center><a href=\"?act=edit&id=".$archives[$i][id]."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=del&id=".$archives[$i][id]."&date=".$date."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
			}
		}
		else {
			echo "<div class=\"header\">".$getdate." kayıtlı yazılarınıza ait yorumlar ..</div><br>";
			?>
			<table class="post" border="0" height="96" width="100%">
				<tbody class="posts">
					<tr><th width="68%"><img src="images/m_down.png">Başlık</th><th width="3%" align="center">YA</th><th width="7%" align="center">Tarih</th><th width="23%" align="center">Kategori(ler)</th></tr>
			<?
			for ($i=0; $i<count($archives); $i++){
				if ($eid<>$archives[$i][id]) $st="none"; else $st="block";
				echo "<tr><td><a href=\"#\" onclick=\"toggleVisibility(document.getElementById('".$archives[$i][id]."'), this); return false\"><img src=\"images/down.png\">".$archives[$i][title]."</a>
				<span id=\"".$archives[$i][id]."\" style=\"display:".$st.";\">";
				
				$ii=0;
				if ($comments = get_comments($id,$archives[$i][id],'a')) {
				?>
				<table class="post" border="0" height="96" width="100%">
						<tbody class="posts">
						<tr><th width="25%">Gönderen</th><th width="60%">Yorum</th><th width="10%" align="center">Gözükür</th><th width="4%" align="center">Sil</th></tr>
				<?
					for ($ii=0; $ii<count($comments); $ii++){
						echo "<tr><td>"
						.$comments[$ii][author]
						."</td><td>"
						.$comments[$ii][comment]
						."</td><td>";
						if ($comments[$ii][status]) {$v=0;$img="true.png";} else {$v=1;$img="false.png";}
						echo "<a href=\"?act=com&date=".$date."&x=chs&v=".$v."&id=".$comments[$ii][id]."&eid=".$archives[$i][id]."\"><center><img src=\"images/".$img."\"></center></a></td>"
						."<td><center><a href=\"?act=com&date=".$date."&x=del&eid=".$archives[$i][id]."&id="
						.$comments[$ii][id]
						."\" onClick=\"return confirmSubmit()\">"
						."<img src=\"images/delete.png\"></a></center>"
						."</td></tr>";
					}
				?></tbody></table><?
				}
				
				echo "</span></td><td align=\"center\">".$ii."</td>
				<td align=\"center\">".$archives[$i][date][day]."/".$archives[$i][date][month]."/".$archives[$i][date][year]."</td><td align=\"center\">";
				if ($act_cat=get_cat($archives[$i][id],1)) foreach ($act_cat as $cat_act) echo get_category_name($cat_act).". ";
				//echo "</td><td><center><a href=\"?act=edit&id=".$archives[$i][id]."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=del&id=".$archives[$i][id]."&date=".$date."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
				echo "</td>";
			}
		}
		?>
			</tbody>
		</table>
		<?
	}

/**/	function check_permit($user,$pass){
		global $config;
                $pass = md5($pass);
		$sql_word = "SELECT * FROM {$config['db']['tableprefix']}users WHERE username = '$user' AND passwd = '$pass'";
		$sql_query = mysql_query($sql_word);
		$assoc_arr = mysql_fetch_assoc($sql_query);
		$return_string = $assoc_arr['id'];
		if (empty($sql_query)) return 0;
		else return $return_string;
	}

/**/	function add_entry($author, $cat_id, $title, $text, $date, $opt="add", $status="1",$id=""){
		global $config;
		switch ($opt){
			case "add":
			$sql_word = "INSERT INTO {$config['db']['tableprefix']}entry VALUES ('', '{$title}', '{$text}', '{$date}', '{$author}', '{$status}')";
			$sql_query = @mysql_query($sql_word);$act_id=mysql_insert_id();
			break;
			case "update":
			$sql_word = "UPDATE {$config['db']['tableprefix']}entry SET title='{$title}', entry='{$text}', status='{$status}' WHERE author = '$author' AND id='$id'";
			$sql_query = @mysql_query($sql_word);$act_id=$id;
			break;
		}
		if($sql_query){$return_value = $act_id; act_cat($cat_id,$act_id);}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}

/**/	function add_cat($cat,$desc,$opt="add",$id="") {
		global $config;
		switch ($opt){
			case "add":
			$sql_word = "INSERT INTO {$config['db']['tableprefix']}category VALUES ('','0', '{$cat}', '{$desc}')";
			break;
			case "update":
			$sql_word = "UPDATE {$config['db']['tableprefix']}category SET name='{$cat}', description='{$desc}' WHERE id='$id'";
			break;
		}
		$sql_query = @mysql_query($sql_word);
		if($sql_query){$return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}

/**/	function add_user($name,$username,$email,$password,$opt="add",$id="") {
		global $config;
                $passwd = md5($password);
		switch ($opt){
			case "add":
			$sql_word = "INSERT INTO {$config['db']['tableprefix']}users VALUES ('','{$username}','{$name}','{$passwd}', '{$email}','2')";
			break;
			case "update":
			$sql_word = "UPDATE {$config['db']['tableprefix']}users SET name='{$name}', username='{$username}', passwd='{$passwd}', email='{$email}' WHERE id='$id'";
			break;
		}
		$sql_query = @mysql_query($sql_word);
		if($sql_query){$return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}

/**/	function del_cat($id){
		global $config;
		$sql_word = "DELETE FROM {$config['db']['tableprefix']}category WHERE id='{$id}'";
		$sql_query = @mysql_query($sql_word);
		if($sql_query){
			$sql_word   = 	"DELETE FROM {$config['db']['tableprefix']}category_act WHERE cat_id='{$id}'";
			$sql_query2 = 	@mysql_query($sql_word);
			if ($sql_query2) $return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}
	
/**/	function del_user($id){
		global $config;
		$sql_word = "DELETE FROM {$config['db']['tableprefix']}users WHERE id='{$id}'";
		$sql_query = @mysql_query($sql_word);
		if($sql_query){$return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}



/**/	function check_cat($cat_id,$entry_id){
		global $config;
		$sql_word = "SELECT id FROM {$config['db']['tableprefix']}category_act WHERE cat_id = '$cat_id' AND entry_id = '$entry_id'";
		$sql_query = @mysql_query($sql_word);
		$number = @mysql_num_rows($sql_query);
		return $number;
	}

/**/	function del_entry($author, $id){
		global $config;
		$sql_word = "DELETE FROM {$config['db']['tableprefix']}entry WHERE author='{$author}' AND id='{$id}'";
		$sql_query = @mysql_query($sql_word);
		if($sql_query){
			$sql_word   = 	"DELETE FROM {$config['db']['tableprefix']}category_act WHERE entry_id='{$id}'";
			$sql_query2 = 	@mysql_query($sql_word);
			if ($sql_query2) $return_value = "1";}
		elseif(!$sql_query){$return_value = "0";}
		else{$return_value = "0";}
		return $return_value;
	}


/**/	function get_users($id="") {
	global $config;

		$sql_word = "SELECT * FROM {$config['db']['tableprefix']}users";
		$sql_query = @mysql_query($sql_word);
		
		for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
				$assoc_arr = mysql_fetch_assoc($sql_query);
				$return_array[$i] = $assoc_arr;
		}

				?>
				<div class="header">Kullanıcıları düzenleyin ..</div><br>
				<table class="post" border="0" height="96" width="100%">
					<tbody class="posts">
						<tr><th width="5%">ID</th><th width="23%">Adı Soyadı</th><th width="18%">Kullanıcı Adı</th><th width="25%">E-Mail</th><th width="15%">Parola</th><th width="8%" align="center">Düzenle</th><th width="7%" align="center">Sil</th></tr>
				<?
				for ($i=0; $i<count($return_array); $i++){
					if ($id==$return_array[$i]['id']){
					echo "<form method=\"POST\" action=\"?act=users&x=upd\">
						<input type=\"hidden\" name=\"id\" value=\"".$return_array[$i]['id']."\">
					      <tr>
						<td>".$return_array[$i]['id']."</td>
						<td><input type=\"text\" name=\"name\" size=\"20\" value=\"".$return_array[$i]['name']."\"></td>
						<td><input type=\"text\" name=\"uname\" size=\"10\" value=\"".$return_array[$i]['username']."\"></td>
						<td><input type=\"text\" name=\"email\" size=\"25\" value=\"".$return_array[$i]['email']."\"></td>
						<td><input name=\"password\" size=\"10\" type=\"password\" value=\"{$return_array[$i]['password']}\"></td>
						<td><center><input type=\"submit\" value=\"Güncelle\"></center></td><td><center><a href=\"?act=cat&x=del&id=".$return_array[$i]['id']."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
					}
					else {
					echo "<tr>
						<td>".$return_array[$i]['id']."</td>
						<td>".$return_array[$i]['name']."</td>
						<td>".$return_array[$i]['username']."</td>
						<td>".$return_array[$i]['email']."</td>
						<td>password :p</td>
						<td><center><a href=\"?act=users&id=".$return_array[$i]['id']."\"><img style=\"vertical-align:none;\" src=\"images/edit.png\"> </a></center></td><td><center><a href=\"?act=users&x=del&id=".$return_array[$i]['id']."\" onClick=\"return confirmSubmit()\"><img style=\"vertical-align:none;\" src=\"images/delete.png\"></a></center></td></tr>";
					}
				}
				if (!$id) {
				?>
				<form method="POST" action="?act=users&x=add">
				<tr><TD>Yeni :</TD>
				<td><input type="text" name="name" size="20"></td>
				<td><input type="text" name="uname" size="10"></td>
				<td><input type="text" name="email" size="25"></td>
				<td><input type="text" name="password" size="10"></td>
				<td colspan="2"><center><input type="submit" value="Ekle"></center></td></tr></form>
				<?
				}
				echo "</tbody></table>";
	}

?>
