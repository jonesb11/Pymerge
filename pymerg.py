from PyPDF2 import PdfFileMerger
import PySimpleGUI as PGUI
import os.path

PGUI.theme('Purple')

file_list_column = [
    [
        PGUI.Text("PDFS Folder"),
        PGUI.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        PGUI.FolderBrowse(),
    ],
    [
        PGUI.Listbox(
            values=[], enable_events=True, size=(45, 20), key="-FILE LIST-"
        )
    ],
        [
        PGUI.Text("MergeName"),
        PGUI.In(size=(25,1), enable_events=True, key="-NAME-"),
        PGUI.Push(),
        PGUI.Button("Merge")
    ],
]

# ----- Full layout -----
layout = [
    [
        PGUI.Column(file_list_column),
    ]
]

window = PGUI.Window("PDF Merger v0.1", layout)

def merge_pdf(FPath, PDFName):
    try:
        os.chdir(FPath)
    except:
        print("Not valid path")
        return

    pdfs = os.listdir()

    merger = PdfFileMerger()

    for pdf in pdfs:
        if(".pdf" not in pdf):
            continue

        merger.append(pdf)

    merger.write(PDFName)
    merger.close()

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == PGUI.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        print(folder)
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".pdf"))
        ]
        window["-FILE LIST-"].update(fnames)

    if event == "-NAME-":
        pdfName = values["-NAME-"]

    if event == "Merge":
        try:
            FPath = folder
        except:
            print("Folder not selected")
            continue

        try:
            PDFName = pdfName
            if(".pdf" not in PDFName):
                PDFName = PDFName + ".pdf"
        except:
            PGUI.popup_error("Please enter a unique name for PDF")
            continue

        if(PDFName != ""):
            merge_pdf(FPath, PDFName)