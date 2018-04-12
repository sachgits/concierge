# Testing Concierge using SAML2

Testing the SAML connection makes use of [**Docker Test SAML 2.0 Identity Provider (IdP)**](https://hub.docker.com/r/kristophjunge/test-saml-idp/) by Kristoph Junge.

To accommodate for testing the SAML2 connection, four imaginary organisations have been set up, each being executed in their own docker container.

There are three scripts available for starting and stopping the containers:

<table>

<tbody>

<tr>

<td>**start.sh**</td>

<td>Starts all four containers</td>

</tr>

<tr>

<td>**stop.sh**</td>

<td>Stops all four containers</td>

</tr>

<tr>

<td>**restart.sh**</td>

<td>Stops and starts all four containers</td>

</tr>

</tbody>

</table>

* * *

<table>

<tbody>

<tr>

<th>Organisation</th>

<th>Network</th>

<th>Users</th>

</tr>

<tr>

<td>

<table>

<tbody>

<tr>

<td>**Blue**</td>
</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>protocol</th>

<th>port number</th>

</tr>

<tr>

<td>http</td>

<td>8180</td>

</tr>

<tr>

<td>https</td>

<td>8543</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>user</th>

<th>password</th>

<th>email address</th>

</tr>

<tr>

<td>bibi</td>

<td>bibi1234</td>

<td>bibi@blue.org</td>

</tr>

<tr>

<td>bert</td>

<td>bert1234</td>

<td>bert@blue.org</td>

</tr>

</tbody>

</table>

</td>

</tr>

<tr>

<td>

<table>

<tbody>

<tr>

<td>**Green**</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>protocol</th>

<th>port number</th>

</tr>

<tr>

<td>http</td>

<td>8280</td>

</tr>

<tr>

<td>https</td>

<td>8643</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>user</th>

<th>password</th>

<th>email address</th>

</tr>

<tr>

<td>gina</td>

<td>gina1234</td>

<td>gina@green.org</td>

</tr>

<tr>

<td>greg</td>

<td>greg1234</td>

<td>greg@green.org</td>

</tr>

</tbody>

</table>

</td>

</tr>

<tr>

<td>

<table>

<tbody>

<tr>

<td>**Red**</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>protocol</th>

<th>port number</th>

</tr>

<tr>

<td>http</td>

<td>8380</td>

</tr>

<tr>

<td>https</td>

<td>8743</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>user</th>

<th>password</th>

<th>email address</th>

</tr>

<tr>

<td>rose</td>

<td>rose1234</td>

<td>rose@red.org</td>

</tr>

<tr>

<td>ralf</td>

<td>ralf1234</td>

<td>ralf@red.org</td>

</tr>

</tbody>

</table>

</td>

</tr>

<tr>

<td>

<table>

<tbody>

<tr>

<td>**Yellow**</td>
</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>protocol</th>

<th>port number</th>

</tr>

<tr>

<td>http</td>

<td>8480</td>

</tr>

<tr>

<td>https</td>

<td>8843</td>

</tr>

</tbody>

</table>

</td>

<td>

<table>

<tbody>

<tr>

<th>user</th>

<th>password</th>

<th>email address</th>

</tr>

<tr>

<td>yvet</td>

<td>yvet1234</td>

<td>yvet@yellow.org</td>

</tr>

<tr>

<td>yves</td>

<td>yves1234</td>

<td>yves@yellow.org</td>

</tr>

</tbody>

</table>

</td>

</tr>

</tbody>

</table>

* * *

## Configuration

### Service Provider configuration
The Service Provider configuration (Concierge that is) is defined in **config.py**. For testing purposes the configuration provided in **config.example.py** may be used.

### Identity Provider configuration
The Identity Provider configurations are done at the admin panel. Add four IdentityProviders and assign the following values to each of them:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Value (#### = http port)</th>

</tr>

<tr>

<td>Shortname</td>

<td>Unique Identity Provider name e.g. _yellow_</td>

<td></td>

</tr>

<tr>

<td>Displayname</td>

<td>Identity Provider name as shown to the users e.g. _The Yellow organisation_</td>

<td></td>

</tr>

<tr>

<td>Metadata url</td>

<td>http://localhost:####/simplesaml/saml2/idp/metadata.php</td>

<td></td>

</tr>

<tr>

<td>Metadata filename</td>

<td>_( Leave empty )_</td>

<td></td>

</tr>

<tr>

<td>Perform slo</td>

<td>Controles whether the SingleLogout service is to be performed</td>

<td></td>

</tr>

</tbody>

</table>

### Idp Email Domain configuration
The Idp Email Domain configurations are also done at the admin panel. Connect each valid email domain with it's accompanying Identity Provider. E.g. **yellow.org** with **yellow**
