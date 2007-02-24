<?php
ob_start();

echo "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>";
include_once("globals.php");

// set record limitations
if($_GET['start']){$start = $_GET['start']; $end = ($_GET['start']+$config['core']['postsinfeed']);}
else{$start = '0'; $end = $config['core']['postsinfeed'];}

db_connection('connect', $config['db']['hostname'].':'.$config['db']['port'], $config['db']['username'], $config['db']['password'], $config['db']['databasename'], $config['db']['connectiontype']);
$posts = get_posts($id, $_GET['cat'], $_GET['date'], $_GET['author'], "1", $start, $end, "db2rss");
db_connection("disconnect");

// set content-type to xml
Header("Content-type: text/xml; charset=utf-8");
?>
<!-- generator="FasaFiso Feed Engine/FasaFiso v<?=$config['fasafiso']['version']?>" -->
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title><?=$config['core']['blogname']?></title>
    <link><?=$config['core']['webaddress']?></link>
    <description><?=$config['core']['blogdesc']?></description>
    <pubDate><?php echo date("r"); ?></pubDate>
    <generator>http://fasafiso.org/?version=<?=$config['fasafiso']['version']?></generator>    
    <?php for($i = 0; $i < count($posts); $i++){ ?>
    <item>
        <title><?=$posts[$i]['title']?></title>
        <link><?=$config['core']['webaddress']?>?id=<?=$posts[$i]['id']?></link>
        <comments><?=$config['core']['webaddress']?>?id=<?=$posts[$i]['id']?>#comments</comments>
        <pubDate><?=$posts[$i]['date']?></pubDate>
        <dc:creator><?=$posts[$i]['author']?></dc:creator>
        <?php for($j = 0; $j < count($posts[$i]['category']); $j++){ echo '<category>'.$posts[$i]['category'][$j]['name'].'</category>'; } ?>

        <guid isPermaLink="true"><?=$config['core']['webaddress']?>?id=<?=$posts[$i]['id']?></guid>
        <description><?=htmlspecialchars(strip_tags($posts[$i]['entry']), ENT_QUOTES)?></description>
        <content:encoded><?=htmlspecialchars($posts[$i]['entry'], ENT_QUOTES)?></content:encoded>
        <? /*<wfw:commentRSS>commentsrss</wfw:commentRSS>*/ ?>
    </item>
    <?php } ?>
</channel>
</rss>
<?
ob_end_flush();
?>