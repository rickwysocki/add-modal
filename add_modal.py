"""
from pathlib import Path

# Folder containing your HTML files
HTML_FOLDER = Path(".")

# Declare the HTML to be included as the modal.
MODAL_HTML = r'''
<div id="site-modal" class="site-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div class="site-modal__content">
        <button class="site-modal__close" type="button" aria-label="Close modal">
            &times;
        </button>

        <h2 id="modal-title">A note from <cite>Kairos</cite></h2>
        <p>This is a local directory containing a piece published by <cite><a href="https://kairos.technorhetoric.net">Kairos: A Journal of Rhetoric, Technology, and Pedagogy</a></cite> When possible, we ask that this piece be asked through the official journal hosted online.</p>
    </div>
</div>
'''

# Declare the Javascript for the modal.
MODAL_JS = r'''
<script>
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("site-modal");
    const closeButton = document.querySelector(".site-modal__close");

    if (!modal || !closeButton) return;

    function closeModal() {
        modal.classList.add("is-hidden");
    }

    closeButton.addEventListener("click", closeModal);

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});
</script>
'''

def inject_modal(html):
    # Avoid adding the modal more than once
    if 'id="site-modal"' in html:
        return html

    # Add link to modal stylesheet above </head>
    position = html.lower().rfind("</head>")
    return html[:position] + "<link rel=\"stylesheet" href="modal-styles.css\">" + "\n" + html[position:]


    additions = MODAL_HTML + MODAL_JS

    # Insert before </body> if it exists
    if "</body>" in html.lower():
        position = html.lower().rfind("</body>")
        return html[:position] + additions + "\n" + html[position:]

    # Otherwise append to the end of the file
    return html + "\n" + additions

def main():
    confirmDir = input("Running this program will edit the contents of your current directory, adding popup text to every HTML page that reminds readers of the official location of the webtext on Kairos servers. Have you ensured that you are working in a COPY of the webtext directory, and not the one included the published production files? (y/n): ")

    if confirmDir == "y":
        for html_file in HTML_FOLDER.rglob("*.html"):
            original = html_file.read_text(encoding="utf-8")

        updated = inject_modal(original)

        if updated != original:
            # Create a backup
            backup_file = html_file.with_suffix(html_file.suffix + ".bak")
            backup_file.write_text(original, encoding="utf-8")

            html_file.write_text(updated, encoding="utf-8")
            print(f"Updated: {html_file}")
        else:
            print(f"Skipped: {html_file}")

    else:
        print("Program aborted.")
    
main()
"""

# import pathlib
from pathlib import Path

# Variables
current_directory = Path.cwd()

p = Path('.')

files = list(Path('.').glob('**/*.txt'))# html_files = [x for x in p if x.is_file()]

cssContent = r'''
.site-modal {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: white;
}

.site-modal__content {
    position: relative;
    width: min(500px, 100%);
    padding: 30px;
    background: white;
    color: #222;
}

.site-modal__close {
    position: absolute;
    top: 8px;
    right: 12px;
    border: 0;
    background: transparent;
    color: #555;
    cursor: pointer;
    font-size: 28px;
    line-height: 1;
}

.site-modal__close:hover {
    color: #000;
}

.site-modal.is-hidden {
    display: none;
}
'''

jsContent = r'''
<script>
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("site-modal");
    const closeButton = document.querySelector(".site-modal__close");

    if (!modal || !closeButton) return;

    function closeModal() {
        modal.classList.add("is-hidden");
    }

    closeButton.addEventListener("click", closeModal);

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});
</script>

'''
# Functions

# Inform user of cwd
def currentDir():
    print("Your current working directory is: " + str(Path.cwd()) + ". Do you want to continue?")

# List HTML files that will be altered.
def listFiles():
    # print("The following files will be affected: " + str(files))
    file_list = [str(file) for file in files]
    print("The following files will be altered: " + str(file_list))
    
# Get user confirmation.
def userConfirm():
    confirmation = input("Are you absolutely sure you want to continue? This cannot be undone. (y/n): ")
    if confirmation == "y":
        print("You selected yes.")
    else:
        print("Program aborted.")

# Create and populate CSS file.
def generateCSS():
    css_file = p / "kairos-modal.css"
    css_file.touch()
    css_file.write_text(cssContent)

# Create and populate JS file.
def generateJS():
    js_file = p / "kairos-modal.js"
    js_file.touch()
    js_file.write_text(jsContent)
        
# Main
def main ():

    currentDir()

    listFiles()

    userConfirm()
    
    generateCSS()
    
    generateJS()

    # Read through HTML files. TODO: Break up this function so that it returns after each injection.

    def inject_modal(html):
        # Avoid adding the modal more than once
        if 'id="site-modal"' in html:
            return html

        # Function 1: Return after stylesheet link injection.
        position = html.lower().rfind("</head>")
        return html[:position] + "<link rel=\"stylesheet" href="modal-styles.css\">" + "\n" + html[position:]


    # Function 2: Return after html and JS injections
    additions = MODAL_HTML + MODAL_JS
    
    # Insert before </body> if it exists
    if "</body>" in html.lower():
        position = html.lower().rfind("</body>")
        return html[:position] + additions + "\n" + html[position:]

    # Otherwise append to the end of the file
    return html + "\n" + additions

        

        





        
    # write modal into HTML pages

    # write Javascript into HTML pages


main()
