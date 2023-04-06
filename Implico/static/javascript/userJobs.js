function searchBarResults() {
    var input = document.getElementById("searchBar");
    var filter = searchBar.value.toLowerCase();
    console.log(filter)

    //HTML DOM Elements - arrays
    var jobContainers = document.getElementsByClassName("jobContainer");
    var titles = document.getElementsByClassName("jobPosition");
    var companies = document.getElementsByClassName("companyName");
    var locations = document.getElementsByClassName("location");
    var salaries = document.getElementsByClassName("salary");
    var tags = document.getElementsByClassName("tags");

    //filtering for loop
    for(let i = 0; i < jobContainers.length; i++){
        let block = jobContainers[i];
        let title = titles[i].innerHTML.toLowerCase();
        let comp = companies[i].innerHTML.toLowerCase();
        let loc = locations[i].innerHTML.toLowerCase();
        let sal = salaries[i].innerHTML.toLowerCase();
        // let tags = tags[i].innerHTML.toLowerCase();
        if((title.includes(filter)) || (comp.includes(filter)) || (loc.includes(filter)) || (sal.includes(filter))){
            block.style.display = "";
        }
        else
            block.style.display = "none";
    }

}