<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',
        'rose:rose1234' => array(
            'uid' => array('1'),
            'eduPersonAffiliation' => array('group1'),
            'emailaddress' => 'rose@red.org',
            'givenname' => 'Rose',
            'surname' => 'Rouge'
        ),
        'ralf:ralf1234' => array(
            'uid' => array('2'),
            'eduPersonAffiliation' => array('group2'),
            'emailaddress' => 'ralf@red.org',
            'givenname' => 'Ralf',
            'surname' => 'Red'
        ),
    ),

);

