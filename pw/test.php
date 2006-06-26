<?php

    // Test Cases

    require_once('classes.php');

    $Pages = Array ('Title','Content','PType');
    $Values= Array ('Baslik','Icerik','D');
    $PP = new Pardus();
    $PP->DbLogDetail = 3;
    $PP->DbConnect('127.0.0.1','root','gooksel','Pardus');
    $PP->UpdateField('Pages','Title','Pardus 1.5',3);
    $PP->InsertRecord('Pages',$Pages,$Values);
    $Records = $PP->GetRecord('Pages','Content',5);
    print_r($Records);
    $Records = $PP->FindRecord('Pages','Title','some','*');
    print_r($Records);

?>
