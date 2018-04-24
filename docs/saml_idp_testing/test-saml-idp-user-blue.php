<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',
        'bibi:bibi1234' => array(
            'uid' => array('1'),
            'eduPersonAffiliation' => array('group1'),
            'emailaddress' => 'bibi@blue.org',
            'name' => 'Bibi Bleu',
        ),
        'bert:bert1234' => array(
            'uid' => array('2'),
            'eduPersonAffiliation' => array('group2'),
            'emailaddress' => 'bert@blue.org',
            'name' => 'Bert Blue',
        ),
    ),

);

