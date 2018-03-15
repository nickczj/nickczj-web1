var Delta = Quill.import('delta');
var quill = new Quill('#editor-container', {
  modules: {
    toolbar: true
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'
});

// Store accumulated changes
var change = new Delta();
quill.on('text-change', function(delta) {
  change = change.compose(delta);
});

// Save periodically
setInterval(function() {
  if (change.length() > 0) {
    console.log('Saving changes', change);

    $.post('/your-endpoint', {
      doc: JSON.stringify(quill.getContents())
    });
    
    console.log(quill.getContents());
    change = new Delta();
  }
}, 5*1000);

// Check for unsaved data
window.onbeforeunload = function() {
  if (change.length() > 0) {
    return 'There are unsaved changes. Are you sure you want to leave?';
  }
};

var form = document.querySelector('form');
form.onsubmit = function() {
  // Populate hidden form on submit
  var note = document.querySelector('input[name=note]');
  note.value = JSON.stringify(quill.getContents());
  
  console.log("Submitted", $(form).serialize(), $(form).serializeArray());
  
  // No back end to actually submit to!
  alert('Open the console to see the submit data!');
  return false;
};
