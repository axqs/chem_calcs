from pyscript import document
from pyweb import pydom
import scipy

to_find = ""
vars = ["p", "v", "n","r", "t"]

def clear(var):
    global to_find
    to_find = var
    document.getElementById("output").innerHTML = ""
    document.getElementById("output").style.border = "none"
    document.getElementById("input_boxes").innerHTML = ""
    return [v for v in vars if v != to_find]

def show_inputs(vars):
    for v in vars:
        label = document.createElement('label')
        
        label.htmlFor = v

        input = document.createElement('input')
        input.type = "text"
        input.id = v
        
        if v == "n":
            label.innerText = v + ": "
            input.placeholder = v
        else:
            label.innerText = v.capitalize() + ": "
            input.placeholder = v.capitalize()

        document.getElementById("input_boxes").append(label)
        if v == "r":
            document.getElementById("input_boxes").append(str(scipy.constants.R) + " J/(K)(mol)")
        else:
            document.getElementById("input_boxes").append(input)
        document.getElementById("input_boxes").append(document.createElement('br'))
        

    document.getElementById("calculate").style.display = "initial"

def solvep(event):
    show_inputs(clear("p"))

def solvev(event):
    show_inputs(clear("v"))

def solven(event):
    show_inputs(clear("n"))

def solvet(event):
    show_inputs(clear("t"))

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

            if to_find == "p":
                euqation = (elements["n"] * scipy.constants.R * elements["t"])/elements["v"]
                unit = "kPa"
            elif to_find == "v":
                euqation = (elements["n"] * scipy.constants.R * elements["t"])/elements["p"]
                unit = "L"
            elif to_find == "n":
                euqation = (elements["p"] * elements["v"])/(elements["t"] * scipy.constants.R)
                unit = "mol"
            elif to_find == "t":
                euqation = (elements["p"] * elements["v"])/(elements["n"] * scipy.constants.R)
                unit = "K"
            
            output_div.style.border = "2px solid red"
            output_div.style.padding = "12px 20px 12px 20px"
            output_div.style.width = "fit-content"
            output_div.innerText = "Result: " + str(round(euqation,2)) + " " + unit

        except ValueError:
            document.getElementById("output").style.border = "none"
            output_div.innerText = "Please ensure all inputs are numbers."