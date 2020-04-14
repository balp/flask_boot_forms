function myPeriodicMethod() {
    $.ajax({
        dataType: "json",
        url: "/random",
        success: function (data) {
            console.log(data);
            $("#roll_value").text(data.random);
            $("#hit_value").text(data.hits);

        },
        complete: function () {
            setTimeout(myPeriodicMethod, 10000);
        }
    });
}

// schedule the first invocation:
setTimeout(myPeriodicMethod, 1000);
