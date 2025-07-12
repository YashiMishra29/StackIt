document.addEventListener('DOMContentLoaded', function() {
    // Initialize Quill editor for ask question form
    if (document.getElementById('editor-container')) {
        const quill = new Quill('#editor-container', {
            theme: 'snow',
            modules: {
                toolbar: [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'header': 1 }, { 'header': 2 }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'script': 'sub'}, { 'script': 'super' }],
                    [{ 'indent': '-1'}, { 'indent': '+1' }],
                    [{ 'direction': 'rtl' }],
                    [{ 'size': ['small', false, 'large', 'huge'] }],
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'font': [] }],
                    [{ 'align': [] }],
                    ['clean'],
                    ['link', 'image']
                ]
            },
            placeholder: 'Write your question here...'
        });

        const questionBody = document.getElementById('question-body');
        quill.on('text-change', function() {
            questionBody.value = quill.root.innerHTML;
        });
    }

    // Initialize Quill editor for answer form
    if (document.getElementById('answer-editor-container')) {
        const answerQuill = new Quill('#answer-editor-container', {
            theme: 'snow',
            modules: {
                toolbar: [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'indent': '-1'}, { 'indent': '+1' }],
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                    ['clean'],
                    ['link', 'image']
                ]
            },
            placeholder: 'Write your answer here...'
        });

        const answerBody = document.getElementById('answer-body');
        answerQuill.on('text-change', function() {
            answerBody.value = answerQuill.root.innerHTML;
        });
    }

    // Voting functionality
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const voteSection = this.closest('.vote-cell');
            const voteCount = voteSection.querySelector('.vote-count');
            let count = parseInt(voteCount.textContent);

            if (this.classList.contains('upvote')) {
                count += 1;
            } else if (this.classList.contains('downvote')) {
                count -= 1;
            }

            voteCount.textContent = count;
        });
    });

    // Bookmark functionality
    document.querySelectorAll('.bookmark-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('fas');
            this.classList.toggle('far');
        });
    });

    // Form submissions
    if (document.getElementById('ask-question-form')) {
        document.getElementById('ask-question-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Question submitted!');
            // In a real app, you would send the data to your backend here
        });
    }

    if (document.getElementById('post-answer-form')) {
        document.getElementById('post-answer-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Answer submitted!');
            // In a real app, you would send the data to your backend here
        });
    }

    if (document.getElementById('login-form')) {
        document.getElementById('login-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Login successful!');
            // In a real app, you would authenticate the user here
        });
    }

    if (document.getElementById('register-form')) {
        document.getElementById('register-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Registration successful!');
            // In a real app, you would create a new user account here
        });
    }
});