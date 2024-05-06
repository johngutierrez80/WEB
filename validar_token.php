<?php
// Incluir la función de conexión
require_once "conexion.php";

try {
    // Verificar si se recibió el token del formulario
    if(isset($_POST['token'])) {
        // Obtener la conexión
        $conn = conectarBaseDeDatos();

        // Obtener el token enviado desde el formulario
        $token = $_POST['token'];

        // Consulta SQL utilizando una consulta preparada
        $sql = "SELECT * FROM Archivos WHERE TokenUnico = ?";
        $stmt = $conn->prepare($sql);
        
        // Verificar si la preparación de la consulta fue exitosa
        if ($stmt) {
            $stmt->bind_param("s", $token); // "s" indica que el parámetro es de tipo string
            $stmt->execute();
            $result = $stmt->get_result();

            // Verificar si se encontró algún resultado
            if ($result->num_rows > 0) {
                // El token es válido
                $response = "Token valido: Documento Original!.";
            } else {
                // El token no es válido
                $response = "Token invalido: Documento Falso!.";
            }

            // Cerrar la conexión a la base de datos
            $stmt->close();
        } else {
            // Si hubo un error en la preparación de la consulta, mostrar un mensaje de error
            $response = "Error en la preparación de la consulta.";
        }

        $conn->close(); // Cerrar la conexión a la base de datos
    } else {
        // Si no se recibió el token, mostrar un mensaje de error
        $response = "No se recibió ningún token.";
    }
} catch (mysqli_sql_exception $e) {
    // Captura la excepción de conexión a la base de datos
    http_response_code(500); // Error interno del servidor
    $response = "Error de conexión. Por favor, inténtalo de nuevo más tarde.";
    // Puedes registrar el error detallado en un archivo de registro
    error_log($e->getMessage());
}

// Devolver la respuesta al cliente
echo $response;
?>
