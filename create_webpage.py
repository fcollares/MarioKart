from mario_kart import get_data

def make_table(headings, data):
    headers_row = "<tr>" + "".join(["<th>" + x + "</th>" for x in headings]) + "</tr>"
    row_data = ""
    for row in data:
        row_data += "<tr>" + "".join(["<td>" + str(x) + "</td>" for x in row]) + "</tr>"
    table_string = """
    <thead>
        {}
    </thead>
    <tbody>
        {}
    </tbody>
    """.format(headers_row, row_data)
    return table_string

def table_page(table_data):
    html_string = """
    <!DOCTYPE html>
        <html>
            <head>
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
            <script src="sorttable.js" type="text/javascript"></script>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>

        <body>
            <div class="container">
                <h3 class="center">Mario Kart Character/Vehicle Combinations</h3>
                <h6 class="center">Click table headers to sort by attribute.</h6>
                <table class=" highlight centered responsive-table sortable">
                    {}
                </table>
            </div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        </body>
    </html>
    """.format(table_data)
    with open("index.html","w") as file:
        file.write(html_string)

if __name__ == "__main__":
    headings, data = get_data()
    table_data = make_table(headings, data)
    table_page(table_data)
