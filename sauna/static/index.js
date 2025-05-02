function printSummaries(sauna_data){

    var template_collection = [];
    // parse player summary json into html template node
    for (steamid in sauna_data){
        var template = document.querySelector("#profiles-template").content.cloneNode(true);
        let summ = sauna_data[steamid].summary;
        template.querySelector('#summary-steamid').textContent = summ.steamid;
        template.querySelector('#summary-personaname').textContent = summ.personaname;
        template.querySelector('#summary-profileurl').href = summ.profileurl;
        template.querySelector('#summary-avatarfull').src = summ.avatarfull;
        template.querySelector('#summary-realname').textContent = summ.realname || '[redacted]';  // non-breaking space
        template_collection.push(template);
    }


    // append templates as child to the profiles html div
    let profileSection = document.querySelector("#profiles");
    template_collection.forEach((template) => {
        profileSection.appendChild(template);
    });
}


async function enumerateGames(sauna_data) {

    // read json to get all the appids in everyones library then
    // populate all the info from the games provided and display it

    let library_collection = [];
    Object.keys(sauna_data).forEach((steamid) => {
        library_collection.push(sauna_data[steamid]['library']);
    });
    // flatten 2d array
    library_collection = library_collection.flat();

    // remove duplicate games
    let unique_collection = Array.from(
        new Map(
            library_collection.map(
                obj => [obj.appid, obj]
            )
        ).values()
    );

    console.log(unique_collection)

    // send api request to get appid info
    for (app in unique_collection) {
        let url = `https://store.steampowered.com/api/appdetails?appids=${app}`;

        console.log(`API Steam Store : ${url}`)

        ok_responses = [];
        try {
            const res = await fetch(url);
            let response = await res.json();
            ok_response.push(response);
        } catch (err) {
            console.error(err);
        }
        
        console.log(ok_responses);
        break;
    }
}

// ENTRY POINT
let sauna_data = null;
try {
    const res = await fetch('/sauna/v1/pool');
    sauna_data = await res.json();
} catch (err) {
    console.error(err);
    return;
}

console.log(sauna_data);
return;

printSummaries(sauna_data);
enumerateGames(sauna_data);