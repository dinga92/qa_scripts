from __future__ import print_function
from os import listdir
from os.path import isdir, join


mypath = '.'

dirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

print(dirs)

img = '10.png'

f = open('qa_epi_to_mni.html', 'wa')


header = """
<HTML><HEAD><meta content='text/html;charset=utf-8' http-equiv='Content-Type'>
<meta content='utf-8' http-equiv='encoding'>
<TITLE>QA QC QT Q page</TITLE></HEAD>
"""

i=1
orientation='x'
subjid=2


print(header, file=f)

#def clickable_image(img_path, elem_id):
#    return """
#<input type='checkbox'
#       class='chk '
#       id='%(elem_id)s'
#       name='%(elem_id)s'
#       value=%(elem_id)s
#       onclick='displayFormContents(this.form);mark(lab_%(elem_id)s)'/>
#<label for='%(elem_id)s'>
#  <img class='img' src='%(img_path)s' id='lab_%(elem_id)s'/>
#</label>
#<p>""" %locals()

def image_with_selections(img_path, elem_id):
    return """
    <h1> %(elem_id)s </h1>
    <select name="%(elem_id)s" id="%(elem_id)s" onclick="mark(%(elem_id)s, lab_%(elem_id)s);displaySelectContents(document)" class="select">
    <option value="1">Good<option>
    <option value="2">Suspicious<option>
    <option value="3">Bad<option>
    </select>

    <label for='numbers'>
      <img class='img'
      onclick="addValue('%(elem_id)s');mark(%(elem_id)s,lab_%(elem_id)s);displaySelectContents(document)"
      src='%(img_path)s' id='lab_%(elem_id)s'/>
    </label>
    <p>

    <button onclick="selectItemByValue('%(elem_id)s', 1);mark(%(elem_id)s,lab_%(elem_id)s);displaySelectContents(document)">Good</button>
    <button onclick="selectItemByValue('%(elem_id)s', 2);mark(%(elem_id)s,lab_%(elem_id)s);displaySelectContents(document)">Suspicious</button>
    <button onclick="selectItemByValue('%(elem_id)s', 3);mark(%(elem_id)s,lab_%(elem_id)s);displaySelectContents(document)">Bad</button>
    """ %locals()





for directory in sorted(dirs):
    img_path = join(directory, 'qa_plots', img)
    elem_id = directory
    print(image_with_selections(img_path, elem_id), file=f)
    print('<hr>', file=f)

print("""
Checked boxes : <br>
<textarea class='js-copytextarea', id='txt' rows="8" cols="75"></textarea><br>
<button class='js-textareacopybtn', id='txt'>Copy textarea</button>
<script>

displaySelectContents(document)

function selectItemByValue(elmnt, value){
    elmnt = document.getElementById(elmnt)
    for(var i=0; i < elmnt.options.length; i++){
      if(elmnt.options[i].value == value)
        elmnt.selectedIndex = i;
    }
  }

function addValue(element){
    var number = document.getElementById(element);
    var new_number = parseInt(number.value) + 1;
    if(new_number == 4)
      new_number = 1;
    selectItemByValue(element, new_number);
}

function mark(value_elem, img_elem) {
    value_elem = document.getElementById(value_elem)
    //img_elem = document.getElementById(img_elem)

    if (value_elem.value == 1) {
        img_elem.style.border = '5px solid white';
    } else if (value_elem.value == 2){
        img_elem.style.border = '5px solid blue';
    } else if (value_elem.value == 3){
        img_elem.style.border = '5px solid red';
    } else {
        img_elem.style.border = '';
    }
}

function displaySelectContents(doc) {
  var out = "";
  for (var i = 0, el; el=doc.getElementsByClassName("select")[i]; i++) {
    out = out + el.id + ' ' + el.value + '\\n'
  }
   document.getElementById('txt').value = out
}

var copyTextareaBtn = document.querySelector('.js-textareacopybtn');
 copyTextareaBtn.addEventListener('click', function(event) {
 	var copyTextarea = document.querySelector('.js-copytextarea');
 	copyTextarea.select();

 	try {
 	    var successful = document.execCommand('copy');
 	    var msg = successful ? 'successful' : 'unsuccessful';
 	    console.log('Copying text command was ' + msg)
 	} catch (err) {
 	  console.log('Oops, unable to copy');
 	}
 });

</script>
</BODY></HTML>""", file=f)

f.close()