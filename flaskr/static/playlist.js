// Hide lists view by default
let divs = document.getElementsByClassName('listPlaylists');
for (let x = 0; x < divs.length; x++) {
    let div = divs[x];
    div.style.display = "none";
}

// If displayCards button is clicked, hide list items and display cards
displayCards.addEventListener("click", function (e) {
    let divs = document.getElementsByClassName('cardDisplay');
    for (let x = 0; x < divs.length; x++) {
        let div = divs[x];
        div.style.display = "flex";
    }

    let divs2 = document.getElementsByClassName('listPlaylists');
    for (let x = 0; x < divs2.length; x++) {
        let div = divs2[x];
        div.style.display = "none";
    }
});
// If displayList button is clicked, hide card items and display lists
displayList.addEventListener("click", function (e) {
    let divs = document.getElementsByClassName('cardDisplay');
    for (let x = 0; x < divs.length; x++) {
        let div = divs[x];
        div.style.display = "none";
    }

    let divs2 = document.getElementsByClassName('listPlaylists');
    for (let x = 0; x < divs2.length; x++) {
        let div = divs2[x];
        div.style.display = "inline";
    }
});
// If search term is entered, hide all items that do not contain the search item
srchTerm.addEventListener("input", function (e) {
    let divs = document.getElementsByClassName('playlistIndiv');

    for (let x = 0; x < divs.length; x++) {
        let div = divs[x];
        //let content = div.innerHTML.trim();
        let div_content = div.textContent.toLowerCase();
        //(content);
        if (div_content.includes(this.value.toLowerCase())) {
            div.style.display = "flex";
        }
        else {
            div.style.display = "none";
        }
    }
});

alphabetDown.addEventListener("click", function (e) {
    let divs = document.getElementsByClassName('playlistIndivCard');
    order_array = bubbleSort(arr = divs, compare = compareAlphabetDown)
    for (let x = 0; x < divs.length; x++) {
        divs[order_array[x]].style.order = x;
    }
});

alphabetUp.addEventListener("click", function (e) {
    let divs = document.getElementsByClassName('playlistIndivCard');
    order_array = bubbleSort(arr = divs, compare = compareAlphabetUp)
    for (let x = 0; x < divs.length; x++) {
        divs[order_array[x]].style.order = x;
    }
});

spotifyOrder.addEventListener("click", function (e) {
    let divs = document.getElementsByClassName('playlistIndivCard');
    for (let x = 0; x < divs.length; x++) {
        divs[x].style.order = 0;
    }
});


// Ordering functions
function swap(arr, a, b) {
    let temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
}

const Compare = {
    LESS_THAN: -1,
    BIGGER_THAN: 1
};

function compareAlphabetDown(a, b) {
    let playlist_name_a = a.getElementsByClassName('card-title')[0].textContent
    let playlist_name_b = b.getElementsByClassName('card-title')[0].textContent
    if (playlist_name_a === playlist_name_b) {
        return 0;
    }
    return playlist_name_a < playlist_name_b ? Compare.LESS_THAN : Compare.BIGGER_THAN;
}

function compareAlphabetUp(a, b) {
    let playlist_name_a = a.getElementsByClassName('card-title')[0].textContent
    let playlist_name_b = b.getElementsByClassName('card-title')[0].textContent
    if (playlist_name_a === playlist_name_b) {
        return 0;
    }
    return playlist_name_a > playlist_name_b ? Compare.LESS_THAN : Compare.BIGGER_THAN;
}


// Sorting algorithm
function bubbleSort(arr, compare) {
    const { length } = arr;
    let order_array = [];

    for (let i = 0; i < length; i++) {
        order_array.push(i);
    }
    for (let i = 0; i < length; i++) {
        for (let j = 0; j < length - 1 - i; j++) { // refer to note below
            if (compare(arr[order_array[j]], arr[order_array[j + 1]]) === Compare.BIGGER_THAN) {
                swap(order_array, j, j + 1);
            }
        }
    }
    return order_array;
}

let elem = document.getElementsByClassName('playlistIndivCard');
for (let i = 0; i < elem.length; i += 2) {
    let boxa = elem[i].id;
    let element = document.getElementById(boxa)
    elem[i].addEventListener("mouseouver", function () {
        document.getElementById(el).getElementsByTagName("img")[0].style.filter = 'grayscale(50%)';
        alert()
    });
}

// for (let x = 1; x < divs.length + 1; x++) {
//     let hoverarea = 'playlist_'.concat(toString(x))
//     hoverarea.addEventListener(mouseover, function () {
//         document.getElementById("hoverarea").getElementsByTagName("img")[0].style.filter = 'grayscale(0%)';
//     });

//     hoverarea.addEventListener('mouseout', function () {
//         document.getElementById("hoverarea").getElementsByTagName("img")[0].style.filter = 'grayscale(100%)';
//     });
// }
