# import pathlib
from pathlib import Path

# Variables
current_directory = Path.cwd()
p = Path('.')

# Declare the HTML to be included as the modal.
modalHTML = r'''
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
'''

# Functions

# Inform user of cwd
def currentDir():
    input("Your current working directory is: " + str(Path.cwd()) + ". All HTML files in this directory will be altered. Do you want to continue?" (Y/n))
    
# Get user confirmation.
def userConfirm():
    confirmation = input("Your current working directory is: " + str(Path.cwd()) + ". All HTML files in this directory will be altered. This cannot be undone. Are you absolutely sure you want to continue? (y/n): ")
    if confirmation.lower() == "y":
        return True 
    else:
        return False

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

def inject_modal(html):
    # Avoid adding the modal more than once
    if 'id="site-modal"' in html:
        return html

    external_files_position = html.lower().rfind("</head>")
    html_position = html.lower().rfind("</body>")

    # Insert before </body> if it exists
    if "</body>" in html.lower():
        insertions = [
            (external_files_position, "\n" + "<link rel=\"stylesheet\" href=\"kairos-modal.css\">" + "\n" + "<script src=\"kairos-modal.js\"></script>" + "\n"),
            (html_position, modalHTML + "\n"),
        ]

        for position, content in sorted(insertions, reverse=True):
            html = html[:position] + content + html[position:]
        return html

    # Otherwise append to the end of the file
    return html + "\n" + additions
    
# Define main() program.
def main ():

    if userConfirm():
    
        generateCSS()
    
        generateJS()

        # Read through HTML files. TODO: Break up this function so that it returns after each injection.

        for html_file in p.rglob("*.html"):
            original = html_file.read_text(encoding="utf-8")
            inject_modal(original)
            
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
        print("Program aborted. No changes made.")

# Execute program.
main()
