function printSummaries(sauna_data){

    var template_collection = [];
    // parse player summary json into html template node
    for (player_id in sauna_data['players']){
        var template = document.querySelector("#profiles-template").content.cloneNode(true);
        let summ = sauna_data['players'][player_id]['summary']
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

    // send api request to get appid info
    for (app in sauna_data['unique_games']) {
        let url = `sauna/v1/store/${app}`;

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

async function main() {
    let sauna_data = null;
    try {
        const res = await fetch('/sauna/v1/pool');
        sauna_data = await res.json();
    } catch (err) {
        console.error(err);
        return;
    }

    console.log(sauna_data);

    printSummaries(sauna_data);
    enumerateGames(sauna_data);
}

main();