position = html.lower().rfind("</head>")
return html[:position] + "<link>success.css" + "\n" + html[position:]
