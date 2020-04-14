flask_boot_forms
================

The simplish flask + WTForms + Bootstrap example


Function
--------

This is a simple HTML5 app running in your browser. It's
loaded from the / URL. Have a backend rest-api on /random
where it gets data from the java script.

Each time random is called a new random number is generated
and if it matches the target value. The hit counter is updated.
A simple form can update the target value.


    ,-------.        ,--------.
    |browser|        |myscript|
    |-------|        |--------|
    |-------|        |--------|
    `-------'        `--------'
        |                 |    
        |                 |    
     ,----.   ,---.   ,------. 
     |root|   |app|   |random| 
     |----|---|---|---|------| 
     |----|   |---|   |------| 
     `----'   `---'   `------' 
