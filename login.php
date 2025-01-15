<?php
    session_start();
    if($_SERVER["REQUEST_METHOD"] == "POST"){

        $username = $_POST['email'];
        $password = $_POST['password'];
    
    $db_server = "localhost";
    $db_user = "root";
    $db_pass = "";
    $db_name = "game";

    $conn = new mysqli($db_server, $db_user, $db_pass, $db_name);

    if($conn->connect_error){
        die("Connection failed: ". $conn->connect_error);
    }
    $error_message = "";

    $query = "SELECT * FROM `test` WHERE email = '$username' AND password = '$password'";
    $result = $conn->query($query);
    
    $email_query = "SELECT * FROM `test` WHERE email = '$username'";
    $email_result = $conn->query($email_query);
   

    if($result ->num_rows == 1) {
        //login Sucess
        header("Location: index.html");      
    }
    if($email_result ->num_rows == 1) {
        echo "<script>
                        alert('Incorrect password. Please try again.');
                        setTimeout(function() {
                            window.location.href = 'login.html'; 
                        }, 1000); 
                      </script>";
    }
    else{
        echo "<script>
                        alert('Incorrect password and/or email. Please try again.');
                        setTimeout(function() {
                            window.location.href = 'login.html'; 
                        }, 1000); 
                      </script>";
    }
    $conn->close();

    // Close database connection
    $conn->close();
    }






    ?>