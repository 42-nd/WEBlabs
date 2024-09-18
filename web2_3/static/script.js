function addComment() {
    const commentText = document.getElementById('commentText').value;
    const commentNickName = document.getElementById('commentNickName').value;

    if (commentText.trim() === '') {
        alert('Комментарий не может быть пустым!');
        return;
    }
    if (commentNickName.trim() === '') {
        alert('Ник не может быть пустым!');
        return;
    }

    fetch('/add_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nick: commentNickName,
            comment: commentText
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('commentText').value = '';
        }
    })
    .catch(error => console.error('Ошибка добавления комментария:', error));
}

function loadComments() {
    fetch('/get_comments') 
        .then(response => response.json()) 
        .then(data => {
            let commentsContainer = document.getElementById('comments-container');
            commentsContainer.innerHTML = ''; 

            data.forEach(comment => {
                let commentDiv = document.createElement('div');
                commentDiv.classList.add('comment');
                commentDiv.textContent = comment;
                commentsContainer.appendChild(commentDiv);
            });
        })
        .catch(error => console.error('Ошибка загрузки комментариев:', error));
}

setInterval(loadComments, 5000);