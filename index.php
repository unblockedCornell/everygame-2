<?php
    session_start();
    $db_server = "localhost";
    $db_user = "root";
    $db_pass = "";
    $db_name = "game";
    $conn = ""; 
    $firstname = $_POST['firstname'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $repeat_password = $_POST['repeat_password'];


//Database connection
try{
$conn = new mysqli($db_server, $db_user, $db_pass, $db_name);
if ($conn->connect_error) {
    throw new Exception("Connection failed: " . $conn->connect_error);
}

/*}
catch(mysqli_sql_exception){
    echo"could not connect!";
}*/

$stmt = $conn->prepare("insert into test(firstname, email, password, password_repeat)values(?, ? ,? ,?)");
$stmt->bind_param("ssss", $firstname, $email, $password, $repeat_password);
if($stmt->execute()) {
echo "registration successful go back to login";
header("Location: login.html");}
else {
    echo "Error: " . $stmt->error;
}
$stmt->close();
$conn->close();
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
?>