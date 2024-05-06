<?php
function conectarBaseDeDatos() {
    // Detalles de conexión
    $servername = "localhost";
    $username = "root"; // Nombre de usuario de la base de datos
    $password = ""; // Contraseña de la base de datos
    $database = "Sdh"; // Nombre de la base de datos
    
    // Crear conexión
    $conn = new mysqli($servername, $username, $password, $database);

    // Verificar la conexión
    if ($conn->connect_error) {
        die("Error de conexión: " . $conn->connect_error);
    }

    // Establecer el conjunto de caracteres a utf8
    $conn->set_charset("utf8");

    // Realizar una consulta de prueba
    $sql = "SELECT 1 FROM dual";
    $result = $conn->query($sql);
    if ($result === FALSE) {
        die("Error al realizar la consulta de prueba: " . $conn->error);
    }  
    
    
    // Devolver el objeto de conexión
    return $conn;
}
?>