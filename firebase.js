function save_to_firebase(state_fact, author_name) {
    var fact_object = {
        state_fact: state_fact,
        author_name: author_name
    };

    firebase.database().ref("state-facts").push().set(fact_object).then(
        function(error) {
            console.log("Error: " + error);
        });
}