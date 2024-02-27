function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteCompliment(complimentId) {
  fetch("/delete-compliment", {
    method: "POST",
    body: JSON.stringify({ complimentId: complimentId }),
  }).then((_res) => {
    window.location.href = "/tamar";
  });
}
