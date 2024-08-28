function getOrders() {
    fetch('http://192.168.80.3:5004/api/orders', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        var orderListBody = document.querySelector('#order-list tbody');
        orderListBody.innerHTML = ''; // Clear previous data

        data.forEach(order => {
            var row = document.createElement('tr');

            // Order ID
            var idCell = document.createElement('td');
            idCell.textContent = order.id;
            row.appendChild(idCell);

            // User Name
            var userNameCell = document.createElement('td');
            userNameCell.textContent = order.user_name;
            row.appendChild(userNameCell);

            // User Email
            var userEmailCell = document.createElement('td');
            userEmailCell.textContent = order.user_email;
            row.appendChild(userEmailCell);

            // Total
            var totalCell = document.createElement('td');
            totalCell.textContent = order.total;
            row.appendChild(totalCell);

            // Date
            var dateCell = document.createElement('td');
            dateCell.textContent = new Date(order.created_at).toLocaleString();
            row.appendChild(dateCell);

            // Actions
            var actionsCell = document.createElement('td');

            // View link
            var viewLink = document.createElement('a');
            viewLink.href = `/viewOrder/${order.id}`;
            viewLink.textContent = 'View';
            viewLink.className = 'btn btn-secondary mr-2';
            actionsCell.appendChild(viewLink);

            // Delete link
            var deleteLink = document.createElement('a');
            deleteLink.href = '#';
            deleteLink.textContent = 'Delete';
            deleteLink.className = 'btn btn-danger';
            deleteLink.addEventListener('click', function() {
                deleteOrder(order.id);
            });
            actionsCell.appendChild(deleteLink);

            row.appendChild(actionsCell);

            orderListBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error:', error));
}
