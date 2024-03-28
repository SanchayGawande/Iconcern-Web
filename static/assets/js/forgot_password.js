document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('resetPasswordForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const auth = firebase.auth();
        var email = document.getElementById('email').value;
        auth.sendPasswordResetEmail(email).then(function() {
            alert('Password reset email sent successfully. Please check your inbox.');
        }).catch(function(error) {
            alert('Error: ' + error.message);
        });
    });
});
