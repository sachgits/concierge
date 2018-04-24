<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',
        'gina:gina1234' => array(
            'uid' => array('1'),
            'eduPersonAffiliation' => array('group1'),
            'emailaddress' => 'gina@green.org',
            'name' => 'Gina Vert', 
        ),
        'greg:greg1234' => array(
            'uid' => array('2'),
            'eduPersonAffiliation' => array('group2'),
            'emailaddress' => 'greg@green.org',
            'name' => 'Greg Green',
        ),
    ),

);

