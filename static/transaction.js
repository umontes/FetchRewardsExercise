const http = new XMLHttpRequest();

function get_points(points, payer_name) {
    // document.getElementById("1000_D").innerHTML = "";

    var add_url = "/adding_points/" + points + "/" + payer_name;

    http.open('GET', add_url, true);
    http.onload = function () {
        document.getElementById("points_added").innerHTML = points + " points were added to your account!<br>";
        document.getElementById("points_added").innerHTML += '{"payer": "' + payer_name + '", "points": ' + points + '}'
    }
    http.send();
}