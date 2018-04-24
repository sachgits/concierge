<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',
        'yvet:yvet1234' => array(
            'uid' => array('1'),
            'eduPersonAffiliation' => array('group1'),
            'emailaddress' => 'yvet@yellow.org',
        ),
        'yves:yves1234' => array(
            'uid' => array('2'),
            'eduPersonAffiliation' => array('group2'),
            'emailaddress' => 'yves@yellow.org',
        ),
    ),

);

