<?php

$base = $_SERVER['REQUEST_SCHEME'] . "://" . $_SERVER['SERVER_NAME'];

// ERROR (Checking some required parameters)
if (!$_SERVER['Remote-User'] || !$_SERVER['mail'] || !$_SERVER['Shib-Session-ID'] || !$_SERVER['eppn']) {
    echo "<script type='text/javascript'>";
    echo "window.alert('Permission is invalid');";
    echo "window.location.href='" . $base . "';</script>";
}
$url = $_SERVER['REQUEST_SCHEME'] . "://localhost/weko/shib/login?next=%2F"; // Call the WEKO login API.
$curl = curl_init();
$post_args = [];
$post_args['SHIB_ATTR_USER_NAME'] = $_SERVER['Remote-User'];
$post_args["SHIB_ATTR_EPPN"] = $_SERVER['eppn'];
$post_args["SHIB_ATTR_MAIL"] = $_SERVER['mail'];
$post_args["SHIB_ATTR_SESSION_ID"] = $_SERVER['Shib-Session-ID'];
$post_args["SHIB_ATTR_ROLE_AUTHORITY_NAME"] = $_SERVER['eduPersonAffiliation'] ?? 'Contributor';
$options = array(
    CURLOPT_POST => true,// Method is POST
    CURLOPT_POSTFIELDS => http_build_query($post_args), // Building body data
);
$cookie = tempnam(sys_get_temp_dir(), 'cookie_');
//set options
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($curl, CURLOPT_COOKIESESSION, true);
curl_setopt_array($curl, $options);
curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie);
curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie);
// request
$result = curl_exec($curl);
$info = curl_getinfo($curl);
$errno = curl_errno($curl);
$error = curl_error($curl);
curl_close($curl);
if (CURLE_OK !== $errno) {
    throw new RuntimeException($error, $errno);
}
header("HTTP/1.1 302 Found");
header("Location: " . $base . $result);
