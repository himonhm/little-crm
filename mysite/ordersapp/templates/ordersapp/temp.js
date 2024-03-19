function addSuborderForm() {
    const $suborderForm = document.getElementById("suborderForm");
    const $suborderContainer = document.getElementById("suborderContainer");
    const hr = document.createElement("hr");
    $suborderContainer.appendChild(hr.cloneNode(true));
    $suborderContainer.appendChild($suborderForm.cloneNode(true));
}

function getDataFromAllForms(formQuerySelector) {
    const forms = Array.from(document.querySelectorAll(formQuerySelector));
    const data = forms.map(form => {
        const inputs = Array.from(form.querySelectorAll("input"));
        return inputs.reduce((acc, input) => {
            acc[input.name] = input.value;
            return acc;
        }, {});
    });
    console.log(data);
    return data;
}


document.addEventListener("DOMContentLoaded", () => {
    const $addRowButton = document.getElementById("addRowButton");
    $addRowButton.addEventListener("click", function (event) {
        event.preventDefault();
        addSuborderForm();
    });

    const $submitButton = document.getElementById("submitButton");
    $submitButton.addEventListener("click", function (event) {
        event.preventDefault();
        allData = {
            "order": document.querySelectorAll("#orderForm"),
            "suborders": getDataFromAllForms("#suborderForm")
        }
        console.log(allData);
    });
});