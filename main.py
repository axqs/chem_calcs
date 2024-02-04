from pyscript import document
from pyweb import pydom

to_find = ""
vars = ["q", "m", "cp", "ti", "tf"]

def clear(var):
    global to_find
    to_find = var
    document.getElementById("output").innerHTML = ""
    document.getElementById("output").style.border = "none"
    document.getElementById("input_boxes").innerHTML = ""
    return [v for v in vars if v != to_find]

def show_inputs(vars):
    for v in vars[::-1]:
        label = document.createElement('label')
        if len(v) > 1:
            sub = document.createElement('sub')
            sub.innerHTML = v[1]
            label.append(v.capitalize()[0])
            label.append(sub)
            label.append(": ")
        else:
            label.innerText = v.capitalize() + ": "
        label.htmlFor = v

        input = document.createElement('input')
        input.type = "text"
        input.id = v
        input.placeholder = v.capitalize()

        document.getElementById("input_boxes").prepend(document.createElement('br'))
        document.getElementById("input_boxes").prepend(input)
        document.getElementById("input_boxes").prepend(label)

    document.getElementById("calculate").style.display = "initial"

def solveq(event):
    show_inputs(clear("q"))

def solvem(event):
    show_inputs(clear("m"))

def solvecp(event):
    show_inputs(clear("cp"))

def solveti(event):
    show_inputs(clear("ti"))

def solvetf(event):
    show_inputs(clear("tf"))

def compute(event):
    elements = {}
    output_div = document.querySelector("#output")
    output_div.innerText = ""

    for i in pydom['#input_boxes input']:
        elements[i.id] = (document.getElementById(i.id).value)
        
    if any(e=="" for e in elements.values()):
        document.getElementById("output").style.border = "none"
        output_div.innerText = "Please fill in all boxes."
    else:
        try:
            elements = {k:float(e) for k,e in elements.items()}
            euqation = 0
            unit = ""

            if to_find == "q":
                euqation = elements["m"]*elements["cp"]*abs(elements["tf"]-elements["ti"])
                unit = "J"
            elif to_find == "m":
                euqation = elements["q"]/(elements["cp"]*abs(elements["tf"]-elements["ti"]))
                unit = "g"
            elif to_find == "cp":
                euqation = elements["q"]/(elements["m"]*abs(elements["tf"]-elements["ti"]))
                unit = "J/(g)*("+u'\xb0'+"C)"
            elif to_find == "ti":
                euqation = ((elements["q"]/(elements["m"]*elements["cp"])) - elements["tf"]) * -1
                unit = u'\xb0'+"C"
            elif to_find == "tf":
                euqation = (elements["q"]/(elements["m"]*elements["cp"])) + elements["ti"]
                unit = u'\xb0'+"C"
            
            output_div.style.border = "2px solid red"
            output_div.style.padding = "12px 20px 12px 20px"
            output_div.style.width = "fit-content"
            output_div.innerText = "Result: " + str(round(euqation,2)) + " " + unit

        except ValueError:
            document.getElementById("output").style.border = "none"
            output_div.innerText = "Please ensure all inputs are numbers."