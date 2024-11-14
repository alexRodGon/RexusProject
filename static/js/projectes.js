function mostrarModal(integrantesString, grupoId) {
  // console.log()
    // var integrantesArray = integrantesString.split(",");
    console.log(integrantesString, grupoId);
  
    // var modal = $("#exampleModal");
    // var listGroup = modal.find(".list-group");
    // listGroup.empty();
    
    // // Establecer el ID del grupo en el modal de detalles y en el de agregar miembros
    // $("#exampleModal, #modalAgregarMiembros").find("#grupoIdInput").val(grupoId);
  
    // integrantesArray.forEach(function (integrante) {
    //   var integranteParts = integrante.trim().split(" ");
    //   var integranteName = integranteParts.slice(1).join(" ");
    //   var integranteLink = $("<a>", {
    //     href: "/perfil/" + integranteParts[0],
    //     class: "list-group-item",
    //     text: integranteName,
    //     style: "text-decoration: none; border: none;",
    //     click: function () {
    //       window.location.href = "/perfil/" + integranteParts[0];
    //     },
    //   });
  
    //   var deleteButton = $("<button>", {
    //     type: "button",
    //     class: "btn btn-danger btn-sm",
    //     html: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.5 16.084l-1.403 1.416-4.09-4.096-4.102 4.096-1.405-1.405 4.093-4.092-4.093-4.098 1.405-1.405 4.088 4.089 4.091-4.089 1.416 1.403-4.092 4.087 4.092 4.094z"/></svg>',
    //     click: function () {
    //       eliminarUsuario(integranteParts[0], grupoId);
    //     },
    //   });
  
    //   var integranteItem = $("<div>", {
    //     class: "d-flex justify-content-between align-items-center",
    //   }).append(integranteLink).append(deleteButton);
  
    //   listGroup.append(integranteItem);
    // });
  
    // modal.modal("show");
  }
  
  // function eliminarUsuario(usuarioId, grupoId) {
  //   if (confirm("¿Estás seguro de que quieres eliminar este usuario del grupo?")) {
  //     var form = $("<form>", {
  //       action: "/eliminarUsuarioDelGrupo",
  //       method: "POST",
  //     }).append(
  //       $("<input>", { type: "hidden", name: "usuarioId", value: usuarioId }),
  //       $("<input>", { type: "hidden", name: "grupoId", value: grupoId })
  //     );
  
  //     $("body").append(form);
  //     form.submit();
  //   }
  // }

  function setProyectoId(proyectoId) {
    var modalWindow = document.getElementsByClassName("modal-content")[0];
    var proyectoIdInput = document.querySelector('input[name="proyectoId"]');
  
    if (proyectoIdInput) {
      proyectoIdInput.value = modalWindow.id;
    } else {
      console.error("No se encontró el elemento con nombre 'grupoId'.");
    }
  }
  
  function abrirModalEditarProyecto(proyectoId, nombreProyecto, descripcionProyecto) {
    console.log("Grupo ID:", proyectoId);
    console.log("Nombre del grupo:", nombreProyecto);
    console.log("Descripción del grupo:", descripcionProyecto);
  
  // Llenar campos del formulario en el modal
  var descripcionInput = document.getElementById("descripcionProyectoEditar");
  if (descripcionInput) {
    descripcionInput.value = descripcionProyecto;
  } else {
    console.error("No se encontró el campo de descripción del grupo");
  }

  var nombreInput = document.getElementById("nombreProyectoEditar");
  if (nombreInput) {
    nombreInput.value = nombreProyecto;
  } else {
    console.error("No se encontró el campo de nombre del grupo");
  }

  // Establecer el ID del grupo en un campo oculto si es necesario
  var grupoIdInput = document.getElementById("proyectoIdEditar");
  if (grupoIdInput) {
    grupoIdInput.value = proyectoId;
  } else {
    console.error("No se encontró el campo oculto de ID del grupo");
  }
  // Mostrar el modal
  var modal = document.getElementById("editarProyectoModal");
  if (modal) {
    modal.style.display = "block";
  } else {
    console.error("No se encontró el modal de edición de grupo");
  }
  }

  var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}
  
  // $(document).ready(function () {
  //   $("#modalAgregarMiembros").on("show.bs.modal", function () {
  //     $("#exampleModal").modal("hide");
  //   });
  // });
  

