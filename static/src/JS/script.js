// function fetchData() {
//     const tableElement = document.createElement("table");
//     tableElement.classList.add("table-agent");
//     document.body.appendChild(tableElement);
//
//     fetch("https://valorant-api.com/v1/agents")
//         .then((response) => {
//             return response.json();
//         })
//         .then((data) => {
//             const agents = data.data;
//
//             console.log(agents);
//
//
//             const headerRow = document.createElement("tr");
//             //const uuidHeader = document.createElement("th");
//             const nameHeader = document.createElement("th");
//
//             //uuidHeader.textContent = "UUID"
//             nameHeader.textContent = "NOM";
//
//             const descriptionHeader = document.createElement("th");
//             descriptionHeader.textContent = "ROLE";
//
//             const iconHeader = document.createElement("th");
//             iconHeader.textContent = "ICONE";
//
//             //headerRow.appendChild(uuidHeader)
//             headerRow.appendChild(nameHeader);
//             headerRow.appendChild(descriptionHeader);
//             headerRow.appendChild(iconHeader)
//             tableElement.appendChild(headerRow);
//
//
//             for (const agent of agents) {
//                 if (agent.isPlayableCharacter === true) {
//                     const row = document.createElement("tr");
//
//                     //const uuidCell = document.createElement("td")
//                     //uuidCell.textContent = agent.uuid;
//                     //row.appendChild(uuidCell);
//
//                     // Cellule pour le nom
//                     const nameCell = document.createElement("td");
//                     nameCell.textContent = agent.displayName;
//                     row.appendChild(nameCell);
//
//                     // Cellule pour la description
//                     const roleCell = document.createElement("td");
//                     roleCell.textContent = agent.role.displayName;
//                     row.appendChild(roleCell);
//
//
//                     // Cellule pour la description
//                     const iconCell = document.createElement("td");
//                     const imgIcone = document.createElement("img");
//                     iconCell.classList.add("td-icones");
//                     imgIcone.classList.add("agent-icones");
//                     imgIcone.setAttribute("src", agent.displayIconSmall)
//                     iconCell.appendChild(imgIcone)
//                     row.appendChild(iconCell);
//
//                     tableElement.appendChild(row);
//                 }
//             }
//         })
//         .catch((error) => {
//             console.error('Une erreur s\'est produite : ', error);
//         });
// }


