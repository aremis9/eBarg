document.addEventListener("DOMContentLoaded", () => {
    
    var selectcategory = document.getElementsByClassName('selectcategory')[0]
    var categories = selectcategory.children

    if (selectcategory.value == "") {
        for (category of categories) {
            if (category == categories[0]) {
                continue
            }
            category.style.color = '#212529'
        }
        selectcategory.style.color = '#6c757d'
    }

    selectcategory.addEventListener('change', () => {
        var placeholder = selectcategory.value

        if (placeholder == "") {
            selectcategory.style.color = '#6c757d'
            console.log(placeholder)
        }
        else {
            selectcategory.style.color = '#212529'
            console.log(placeholder)
        }
    })


})