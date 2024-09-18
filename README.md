# AI assistant

> A project for Huawei Hackathon 2023 which required a team to build an AI assistant that accesses data from a database based on plain text prompt

# Authors
- Radek Zajicek - https://github.com/aze-kharini
- Paweł Popkiewicz - https://github.com/PawelPopkiewicz
## Features
- Accessing a database based on a name
- Getting the schemas for tables in the database
- Checking the question prompt
- Using a TEXT->SQL model, generating sqlite code for the question
- Extracting the information from the database
- Formatting the data into readable form
  - Either a table
  - or feeding into a LLM model with the question to convert it into a plain text answer
- Displaying the sql generated to the user

## To-Do
- [ ] SQL checks for injections, hallucinations, DML, DDL
- [ ] Context preservation
- [ ] Performance improvement with different models
- [ ] Fine Tuning the model on specific Data Sets
- [ ] Make it accessible through a webpage
