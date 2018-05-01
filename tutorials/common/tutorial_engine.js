function buttonAction(obj) {
  checkBox = $(obj).find("input[type=checkbox]").closest("input")[0];
  checkBox.checked = true;
  checkBox.disabled = true;
  obj.disabled = true;
  var commands = []
  for (var attr in obj.attributes) {
    if (obj.attributes[attr].name && obj.attributes[attr].name.startsWith("command")) {
      var command = obj.attributes[attr].value;
      commands.push(command)
    }
  }

  var commands_len = commands.length - 1
  for (var counter in commands) {
    var seq_command = commands[counter]+"&_seq="+counter+"/"+commands_len;
    sendCommand(seq_command);
  }
}

function syncPropertyValue(obj){

  var button = $(obj).closest("button");
  var prop_name = obj.attributes["prop_name"].value;
  var node_name = button[0].attributes["node_name"].value;
  var command = "change_prop&node_name="+node_name+"&prop_name="+prop_name+"&value="+obj.value;

  sendCommand(command);
  button.find("[prop_name="+prop_name+"]").each(function(){
    this.value = obj.value;
  });

}

function centerView(){
  var command = "view_all";
  sendCommand(command);
}

function resetView(){
  var command = "clear_node_groups";
  sendCommand(command);
  $(document).find("input[type=checkbox]").each(function(){
    this.checked = false;
    this.disabled = false;
  });
  $(document).find("button[type=button]").each(function(){
    this.disabled = false;
  });
}

function sendCommand(command){
  var BASE_URL = "http://localhost:4000/node/?command=";
  var url = BASE_URL + command;
  console.log(url);

  $.ajax({
       url: url,
       type: "GET",
       success: function(data) {console.log("OK");}
    });

}