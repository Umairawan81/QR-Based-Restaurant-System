updateBtn = document.getElementsByClassName('update-bucket')


for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function() {
        var itemId = this.dataset.product
        var action = this.dataset.action
        console.log('Item id: ', itemId, 'Action: ', action)
        UpdateUserOrder(itemId , action)
    })

    
}

function UpdateUserOrder(itemId,action){

    var URL = '/Update-Item/'; // Here i defined the url where i
    // want to send my productid and action data too .
    fetch(URL, {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken ,
        },
        body: JSON.stringify({'itemId': itemId, 'action': action})
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        console.log('data:' , data)
        alertify.success('Item Added');
    })
    

}