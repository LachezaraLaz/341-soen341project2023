function addExperience() {
    //getting the root element we will be appending the new work experience block to
    var divRoot = document.getElementById("expBlock");

    //creating the div to hold our work experience block
    var divContainer = document.createElement("div");
    divContainer.className = "container p-3 my-3 bg-white text-black border";

    //creating the input for work experience ID
    var expIdInput = document.createElement("input");
    expIdInput.setAttribute('type', 'hidden');
    expIdInput.setAttribute('name', 'expID');
    expIdInput.setAttribute('value', 'new');
    divContainer.appendChild(expIdInput);

    //creating the input for job title
    var formGroupJobTitle = document.createElement("div");
    formGroupJobTitle.className = "form-group";
    //creating label tag for the input of job title
    var labelJobTitle = document.createElement("label");
    labelJobTitle.setAttribute('for', 'jobTitle');
    labelJobTitle.innerHTML = "Job Title:";
    //creating input tag for job title
    var inputJobTitle = document.createElement("input");
    inputJobTitle.className = "form-control";
    inputJobTitle.required;
    inputJobTitle.setAttribute('type', 'text');
    inputJobTitle.setAttribute('name', 'JobTitle');
    inputJobTitle.setAttribute('placeholder', 'Insert Title');
    //appending elements
    formGroupJobTitle.appendChild(labelJobTitle);
    formGroupJobTitle.appendChild(inputJobTitle);
    divContainer.appendChild(formGroupJobTitle);

    //creating the input for employer
    var formGroupEmployer = document.createElement("div");
    formGroupEmployer.className = "form-group";
    //creating label tag for the input of employer
    var labelEmployer = document.createElement("label");
    labelEmployer.setAttribute('for', 'employer');
    labelEmployer.innerHTML = "Employer:";
    //creating input tag for employer
    var inputEmployer = document.createElement("input");
    inputEmployer.className = "form-control";
    inputEmployer.required;
    inputEmployer.setAttribute('type', 'text');
    inputEmployer.setAttribute('name', 'Employer');
    inputEmployer.setAttribute('placeholder', 'Insert Employer');
    //appending elements
    formGroupEmployer.appendChild(labelEmployer);
    formGroupEmployer.appendChild(inputEmployer);
    divContainer.appendChild(formGroupEmployer);

    //creating the input for start date
    var formGroupStartDate = document.createElement("div");
    formGroupStartDate.className = "form-group";
    //creating label tag for the input of start date
    var labelStartDate = document.createElement("label");
    labelStartDate.setAttribute('for', 'startDate');
    labelStartDate.innerHTML = "Start Date:";
    //creating input tag for start date
    var inputStartDate = document.createElement("input");
    inputStartDate.className = "form-control";
    inputStartDate.required;
    inputStartDate.setAttribute('type', 'text');
    inputStartDate.setAttribute('name', 'StartDate');
    inputStartDate.setAttribute('placeholder', 'MM/YYYY');
    inputStartDate.setAttribute('pattern', '^((0[1-9])|(1[0-2]))\/(\d{4})$');

    //appending elements
    formGroupStartDate.appendChild(labelStartDate);
    formGroupStartDate.appendChild(inputStartDate);
    divContainer.appendChild(formGroupStartDate);

    //creating the input for end date
    var formGroupEndDate = document.createElement("div");
    formGroupEndDate.className = "form-group";
    //creating label tag for the input of end date
    var labelEndDate = document.createElement("label");
    labelEndDate.setAttribute('for', 'endDate');
    labelEndDate.innerHTML = "End Date:";
    //creating input tag for end date
    var inputEndDate = document.createElement("input");
    inputEndDate.className = "form-control";
    inputEndDate.required;
    inputEndDate.setAttribute('type', 'text');
    inputEndDate.setAttribute('name', 'endDate');
    inputEndDate.setAttribute('placeholder', 'MM/YYYY');
    inputEndDate.setAttribute('pattern', '^((0[1-9])|(1[0-2]))\/(\d{4})$');
    //appending elements
    formGroupEndDate.appendChild(labelEndDate);
    formGroupEndDate.appendChild(inputEndDate);
    divContainer.appendChild(formGroupEndDate);

    //creating the input for job description
    var formGroupDesc = document.createElement("div");
    formGroupDesc.className = "form-group";
    //creating label tag for the input of job description
    var labelDesc = document.createElement("label");
    labelDesc.setAttribute('for', 'description');
    labelDesc.innerHTML = "Description:";
    //creating input tag for job description
    var inputDesc = document.createElement("input");
    inputDesc.className = "form-control";
    inputDesc.required;
    inputDesc.setAttribute('type', 'text');
    inputDesc.setAttribute('name', 'Description');
    inputDesc.setAttribute('placeholder', 'Insert a description');
    //appending elements
    formGroupDesc.appendChild(labelDesc);
    formGroupDesc.appendChild(inputDesc);
    divContainer.appendChild(formGroupDesc);

    //creating the input for skills
    var formGroupSkills = document.createElement("div");
    formGroupSkills.className = "form-group";
    //creating label tag for the input of skills
    var labelSkills = document.createElement("label");
    labelSkills.setAttribute('for', 'skills');
    labelSkills.innerHTML = "Description:";
    //creating input tag for skills
    var inputSkills = document.createElement("input");
    inputSkills.className = "form-control";
    inputSkills.required;
    inputSkills.setAttribute('type', 'text');
    inputSkills.setAttribute('name', 'Skills');
    inputSkills.setAttribute('placeholder', 'Autonomy, C#, JavaScript, ...');
    //appending elements
    formGroupSkills.appendChild(labelSkills);
    formGroupSkills.appendChild(inputSkills);
    divContainer.appendChild(formGroupSkills);
}