document.addEventListener('DOMContentLoaded', () => {
    window.handleReplySubmit = async (event, commentId) => {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });

            if (response.ok) {
                const data = await response.json();
                
                // Append the new comment or replies to the appropriate container
                const repliesContainer = document.getElementById(`replies-${commentId}`);
                repliesContainer.insertAdjacentHTML('beforeend', data.html);
                
                // Optionally clear the form
                form.reset();
            } else {
                console.error('Failed to submit reply');
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    };
});
