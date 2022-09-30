cupcakeList = document.getElementById('cupcake-list');
addCupcakeBtn = document.getElementById('add-cupcake-button');

flavorInput = document.getElementById('flavor');
ratingInput = document.getElementById('rating');
sizeInput = document.getElementById('size');
imageInput = document.getElementById('image');


addCupcakeBtn.addEventListener('click', createCupcake)

async function getCupcakes() {
    url = "/api/cupcakes"
    const resp = await axios.get(url)
    for( let cupcake of resp.data.cupcakes) {
        li = document.createElement('li');
        li.innerHTML = `${cupcake.flavor}`;
        cupcakeList.append(li);
    }
};
getCupcakes();

async function createCupcake(e) {
    e.preventDefault();

    args = {
        "flavor": flavorInput.value, 
        "rating": ratingInput.value, 
        "size": sizeInput.value, 
        "image": imageInput.value
    }
    url = "/api/cupcakes";
    const resp = await axios.post(url, args);

    if (resp.status === 201){
        li = document.createElement('li')
        li.innerHTML = `${resp.data.cupcake.flavor}`
        cupcakeList.append(li)

        flavorInput.value = "";
        ratingInput .value=  "";
        sizeInput.value = "";
        imageInput.value = "";
    }



}