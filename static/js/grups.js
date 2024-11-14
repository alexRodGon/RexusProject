function mostrarModal(integrantesString, grupoId) {
  var integrantesArray = integrantesString.split(",");
  console.log(integrantesString, grupoId);

  var modal = $("#exampleModal");
  var listGroup = modal.find(".list-group");
  listGroup.empty();
  var modalWindow = document.getElementsByClassName("modal-content")[0];
  console.log(modalWindow);
  modalWindow.id = grupoId;
  console.log(modalWindow);

  // Establecer el ID del grupo en el modal de detalles del grupo
  var grupoIdInput = document.getElementById(grupoId);
  if (grupoIdInput) {
    grupoIdInput.value = grupoId;
  } else {
    console.error("El campo grupoIdInput no se encontró en el DOM.");
  }

  // Establecer el ID del grupo en el modal de agregar miembros
  var modalAgregarMiembros = $("#modalAgregarMiembros");
  var grupoIdInputAgregarMiembros = modalAgregarMiembros.find("#grupoIdInput");
  if (grupoIdInputAgregarMiembros) {
    grupoIdInputAgregarMiembros.val(grupoId);
  } else {
    console.error(
      "El campo grupoIdInput no se encontró en el modal de agregar miembros."
    );
  }

  console.log("si" + grupoId);

  integrantesArray.forEach(function (integrante) {
    var integranteParts = integrante.trim().split(" ");
    var integranteName = integranteParts.slice(1).join(" ");

    var integranteItem = $("<div>", {
      class: "d-flex justify-content-between align-items-center",
    });

    var svgElement = $(
      '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M19 7.001c0 3.865-3.134 7-7 7s-7-3.135-7-7c0-3.867 3.134-7.001 7-7.001s7 3.134 7 7.001zm-1.598 7.18c-1.506 1.137-3.374 1.82-5.402 1.82-2.03 0-3.899-.685-5.407-1.822-4.072 1.793-6.593 7.376-6.593 9.821h24c0-2.423-2.6-8.006-6.598-9.819z"/></svg>'
    );

    var integranteLink = $("<a>", {
      href: "/perfil/" + integranteParts[0],
      class: "list-group-item",
      text: integranteName,
      style: "text-decoration: none; border: none;",
    });

    var containerList = $("<div>", {
      class: "list-group-item d-flex align-items-center",

      css: {
        cursor: "pointer",
        "text-decoration": "none",
        border: "none",
      },
      click: function () {
        window.location.href = "/perfil/" + integranteParts[0];
      },
    });

    containerList.append(integranteLink);
    containerList.prepend(svgElement);

    var svgDelete = $(
      '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.5 16.084l-1.403 1.416-4.09-4.096-4.102 4.096-1.405-1.405 4.093-4.092-4.093-4.098 1.405-1.405 4.088 4.089 4.091-4.089 1.416 1.403-4.092 4.087 4.092 4.094z"/></svg>'
    );

    var deleteButton = $("<button>", {
      type: "button",
      class: "btn btn-danger btn-sm",
      html: svgDelete,
    });

    svgDelete.css({
      width: "1em",
      height: "1em",
      fill: "currentColor",
    });

    deleteButton.on("click", function () {
      eliminarUsuario(integranteParts[0], grupoId);
    });

    integranteItem.append(containerList);
    integranteItem.append(deleteButton);

    listGroup.append(integranteItem);
  });

  modal.modal("show");
}

function eliminarUsuario(usuarioId, grupoId) {
  if (
    confirm("¿Estás seguro de que quieres eliminar este usuario del grupo?")
  ) {
    var form = document.createElement("form");
    form.action = "/eliminarUsuarioDelGrupo";
    form.method = "POST";

    var usuarioIdField = document.createElement("input");
    usuarioIdField.type = "hidden";
    usuarioIdField.name = "usuarioId";
    usuarioIdField.value = usuarioId;
    form.appendChild(usuarioIdField);

    var grupoIdField = document.createElement("input");
    grupoIdField.type = "hidden";
    grupoIdField.name = "grupoId";
    grupoIdField.value = grupoId;
    form.appendChild(grupoIdField);

    document.body.appendChild(form);
    form.submit();
  }
}

function setGrupoId(grupoId) {
  var modalWindow = document.getElementsByClassName("modal-content")[0];
  var grupoIdInput = document.querySelector('input[name="grupoId"]');

  if (grupoIdInput) {
    grupoIdInput.value = modalWindow.id;
  } else {
    console.error("No se encontró el elemento con nombre 'grupoId'.");
  }
}

function abrirModalEditarGrupo(grupoId, nombreGrupo, descripcionGrupo) {
  console.log("Grupo ID:", grupoId);
  console.log("Nombre del grupo:", nombreGrupo);
  console.log("Descripción del grupo:", descripcionGrupo);

  // Llenar campos del formulario en el modal
  var descripcionInput = document.getElementById("descripcionGrupoEditar");
  if (descripcionInput) {
    descripcionInput.value = descripcionGrupo;
  } else {
    console.error("No se encontró el campo de descripción del grupo");
  }

  var nombreInput = document.getElementById("nombreGrupoEditar");
  if (nombreInput) {
    nombreInput.value = nombreGrupo;
  } else {
    console.error("No se encontró el campo de nombre del grupo");
  }

  // Establecer el ID del grupo en un campo oculto si es necesario
  var grupoIdInput = document.getElementById("grupoIdEditar");
  if (grupoIdInput) {
    grupoIdInput.value = grupoId;
  } else {
    console.error("No se encontró el campo oculto de ID del grupo");
  }
  // Mostrar el modal
  var modal = document.getElementById("editarGrupoModal");
  if (modal) {
    modal.style.display = "block";
  } else {
    console.error("No se encontró el modal de edición de grupo");
  }
}

$(document).ready(function () {
  $("#modalAgregarMiembros").on("show.bs.modal", function () {
    $("#exampleModal").modal("hide");
  });
});
