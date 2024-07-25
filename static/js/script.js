// Add your JavaScript code here 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbox</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div id="chatbox-container">
        <div id="chatbox"></div>
        <form id="chatForm">
            <input type="text" id="username" name="username" placeholder="Username" required>
            <input type="text" id="message" name="message" placeholder="Message" required>
            <button type="submit">Send</button>
        </form>
    </div>

    <script>
        $(document).ready(function() {
            function loadMessages() {
                $.getJSON('/get_messages', function(data) {
                    $('#chatbox').empty();
                    for (let msg of data) {
                        $('#chatbox').append(`<div><strong>${msg[0]}:</strong> ${msg[1]} <em>${msg[2]}</em></div>`);
                    }
                });
            }

            $('#chatForm').on('submit', function(e) {
                e.preventDefault();
                $.post('/send_message', $(this).serialize(), function() {
                    $('#message').val('');
                    loadMessages();
                });
            });

            loadMessages();
            setInterval(loadMessages, 5000);
        });
    </script>
</body>
</html>
