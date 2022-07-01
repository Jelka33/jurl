<head>
    <title>JURL Redirect</title>
</head>
<?php
$uri = explode('/', strtok(getenv('REQUEST_URI'), '?'));

if ($uri[1] == ""){
    echo "<script type=\"text/javascript\">
            window.location.replace(\"https://jelka33.github.io/jurl\");
          </script>";
}
elseif (count($uri) > 2){
    http_response_code(404);
    include('error_404.html');
    die();
}
else{
    echo "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script>";
    echo "<script type=\"text/javascript\">
            $.ajax({
                type: 'get',
                url: 'https://jurl.jelka33.repl.co/get-link?code=" . $uri[1] . "',
                success: function(data){
                    console.log(data);
                    if(!data.startsWith(\"https://\") && !data.startsWith(\"http://\")){
                        window.location.replace(\"http://\" + data);
                    }
                    else{
                        window.location.replace(data);
                    }
                }
            });
          </script>";
}
?>
