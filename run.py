#################################################
# Chinese card gen 2
#
# TODO
# - note type 2 templates
#   - move templates to seperate file
# - known words csv and tsv
# 
# 
# 
#
#
#
#
#################################################

note_1_templates = [
    {
      'name': 'Comprehension Card',
      'qfmt': '<div style=\'font-family: Arial; text-align: center; font-size: 40px; color: red;\'>{{Simplified_Word}}/{{Traditional_Word}}</div>',
      'afmt': '{{FrontSide}}<hr id=answer>{{Picture}}<br><br>{{Recording}}<br></div><div style=\'font-family: Arial; font-size: 30px; color: red;\'>{{Pinyin}}</div><br><div style=\'font-family: Arial; font-size: 30px; color: red;\'><br>{{Mnemonic_Classifier}}<br>{{Personal_Connection}}</div>',
    },
    {
      'name': 'Production Card',
      'qfmt': 'How do you pronounce this word?<br><br>{{Picture}}',
      'afmt': '{{FrontSide}}<hr id=answer><div style=\'font-family: Arial; font-size: 30px; color: red;\'>{{Pinyin}}</div><br><div style=\'font-family: Arial; font-size: 40px; color:red;\'>({{Simplified_Word}}/{{Traditional_Word}})</div><br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 30px; color: red;\'><br>{{Mnemonic_Classifier}}<br>{{Personal_Connection}}</div>',
    },
    {
      'name': 'Simplified Stroke 1',
      'qfmt': '<b>Simplified</b><br>{{#S_Char_1}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{S_Char_1}}</div><br>{{/S_Char_1}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Simplified_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Simplified_Word}}<br>{{Simplified_Story}}',
    },
    {
      'name': 'Simplified Stroke 2',
      'qfmt': '<b>Simplified</b><br>{{#S_Char_2}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{S_Char_2}}</div><br>{{/S_Char_2}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Simplified_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Simplified_Word}}<br>{{Simplified_Story}}',
    },
    {
      'name': 'Simplified Stroke 3',
      'qfmt': '<b>Simplified</b><br>{{#S_Char_3}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{S_Char_3}}</div><br>{{/S_Char_3}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Simplified_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Simplified_Word}}<br>{{Simplified_Story}}',
    },
    {
      'name': 'Simplified Stroke 4',
      'qfmt': '<b>Simplified</b><br>{{#S_Char_4}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{S_Char_4}}</div><br>{{/S_Char_4}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Simplified_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Simplified_Word}}<br>{{Simplified_Story}}',
    },
    {
      'name': 'Tradtional Stroke 1',
      'qfmt': '<b>Traditional</b><br>{{#T_Char_1}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{T_Char_1}}</div><br>{{/T_Char_1}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Traditional_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Traditional_Word}}<br>{{Traditional_Story}}',
    },
    {
      'name': 'Tradtional Stroke 2',
      'qfmt': '<b>Traditional</b><br>{{#T_Char_2}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{T_Char_2}}</div><br>{{/T_Char_2}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Traditional_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Traditional_Word}}<br>{{Traditional_Story}}',
    },
    {
      'name': 'Tradtional Stroke 3',
      'qfmt': '<b>Traditional</b><br>{{#T_Char_3}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{T_Char_3}}</div><br>{{/T_Char_3}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Traditional_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Traditional_Word}}<br>{{Traditional_Story}}',
    },
    {
      'name': 'Tradtional Stroke 4',
      'qfmt': '<bTraditional</b><br>{{#T_Char_4}}Stroke order and component parts of this character:<br><br>{{Picture}}<br>{{Recording}}<br><div style=\'font-family: Arial; font-size: 40px; color: red;\'>{{T_Char_4}}</div><br>{{/T_Char_4}}',
      'afmt': '{{FrontSide}}<hr id=answer><div id="target"></div><script type="text/javascript">var characters = "{{Traditional_Word}}".split("")var js = document.createElement("script");js.type = "text/javascript";js.src = "https://cdn.jsdelivr.net/npm/hanzi-writer@2.2/dist/hanzi-writer.min.js";js.onload = function() {for (x of characters) {var writer = HanziWriter.create(\'target\', x, {width: 200,height: 150,padding: 5,  showOutline: true,strokeAnimationSpeed: 1.5, delayBetweenStrokes: 150, // millisecondsradicalColor: \'#337ab7\' // blue});writer.loopCharacterAnimation()};};document.body.appendChild(js);</script>{{Traditional_Word}}<br>{{Traditional_Story}}',
    },
    {
      'name': 'Mnemonic Classifer',
      'qfmt': '{{#Mnemonic_Classifier}}What is this words classifier?<br><br>{{Picture}}<br>{{Simplified_Word}}/{{Traditional_Word}}{{/Mnemonic_Classifier}}',
      'afmt': '{{FrontSide}}<hr id=answer>{{Mnemonic_Classifier}}',
    },
]

print(note_1_templates)