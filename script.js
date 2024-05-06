$(document).ready(function() {
    $('#tokenForm').submit(function(e) {
        e.preventDefault(); // Evita que el formulario se envíe normalmente

        // Muestra la animación de carga
        $('#loadingAnimation').show();

        // Oculta las animaciones de resultado anteriores
        $('#CheckAnimation').hide();
        $('#dangerAnimation').hide();
        $('#warningAnimation').hide();

        var token = $('#token').val();
        var formData = {
            token: token
        };

        // Envía la solicitud AJAX después de un pequeño retraso
        setTimeout(function() {
            $.ajax({
                type: 'POST',
                url: 'validar_token.php',
                data: formData,
                success: function(response) {
                    console.log("Respuesta del servidor:", response);

                    $('#result').html(response);

                    if (response.trim() === 'Token valido: Documento Original!.') {
                        // Muestra la animación de checkmark si el token es válido
                        $('#CheckAnimation').show();
                    } else if (response.trim() === 'Token invalido: Documento Falso!.') {
                        // Muestra la animación de peligro si el token no es válido
                        $('#dangerAnimation').show();
                    } else {
                        // Muestra la animación de advertencia si no se ingresó ningún token
                        $('#warningAnimation').show();
                    }

                    // Limpiar el campo del token
                    $('#token').val('');
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX:", error);
                    $('#tokenError').text('Error al procesar la solicitud.');
                    $('#tokenError').show();
                },
                complete: function() {
                    // Oculta la animación de carga cuando la solicitud AJAX se completa (ya sea con éxito o con error)
                    $('#loadingAnimation').hide();
                }
            });
        }, 500); // Retraso de 500 milisegundos
    });
});
