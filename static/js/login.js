function timeout(ms, promise) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            reject(new Error("timeout"))
        }, ms)
        promise.then(resolve, reject)
    })
}


$('#btnLogin').click(function() {

    user = {
        'email' : $("#inputEmail").val(),
        'password' : $("#inputPassword").val(),
    }

    console.log(user);

    timeout(3000, fetch('http://127.0.0.1:5000/login', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })).then(function(response) {
        console.log(result);
        // process response
    }).catch(function(error) {
        // might be a timeout error
    })


    // var result = fetch('http://127.0.0.1:5000/login', {
    //       method: 'post',
    //       headers: {
    //         'Accept': 'application/json',
    //         'Content-Type': 'application/json'
    //       },
    //       body: JSON.stringify(user)
    //     })

});
