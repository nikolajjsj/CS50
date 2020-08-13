const baseUrl = "https://api.themoviedb.org/3/movie/popular?api_key=bbba80bf20bfe1488d47bebac9557738";
const baseImageUrl = "https://image.tmdb.org/t/p/original";

let imageArray = [];

fetch(baseUrl).then(response => response.json()).then(data => {
    // for loop to loop over all backdrop images of the most popular movies
    for (let i = 0; i < data["results"].length; i++){
        imageArray.push(baseImageUrl + data["results"][i]["backdrop_path"]);
    }

    // log the resulting image array
    console.log(imageArray);

    // pick random backdrop and use that for the newtab.html,
    let backdrop = imageArray[Math.floor(Math.random() * imageArray.length)];

    // set background image for body
    document.body.style.backgroundImage = `url("${backdrop}")`;
});