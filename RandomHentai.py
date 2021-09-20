from hentai import *
import random
import PySimpleGUI as sg
import webbrowser
import requests
from PIL import Image, ImageTk
import io


def TextLabel(text):
    return sg.Text(text + ":", justification="r", size=(15, 1))


languages = ["english", "Chinese", "japanese", "Dont Care"]

sg.theme("DarkGrey3")

layout = [
    [
        sg.Text(
            "Enter Tags like this: big breasts, loli, futa \nClick Result or Cover to open Browser"
        )
    ],
    [
        TextLabel("Tags"),
        sg.Input(key="-TAGS-"),
    ],
    [TextLabel("Excluded Tags"), sg.Input(key="-ETAGS-", default_text=None)],
    [
        TextLabel("Maximum Pages"),
        sg.Spin(
            key="-PAGES-",
            initial_value=0,
            values=[i for i in range(0, 10000)],
            size=(10, 1),
        ),
    ],
    [
        TextLabel("Preffered Language"),
        sg.Combo(languages, key="-LANG-", size=(10, 10), default_value="english"),
    ],
    [
        sg.Button("Search", key="-SEARCH-"),
        sg.Checkbox("Show Cover", key="-COVER-", enable_events=True),
        sg.Input(
            key="-QUERY-",
            use_readonly_for_disable=True,
            disabled=True,
            disabled_readonly_background_color=sg.theme_background_color(),
            disabled_readonly_text_color=sg.theme_text_color(),
            border_width=0,
            expand_x=True,
        ),
        sg.Text(key="-RESULTS-"),
    ],
    [
        sg.Text(
            "URL" + ": ",
        ),
        sg.Input(
            key="-URL-",
            enable_events=True,
            use_readonly_for_disable=True,
            disabled=True,
            disabled_readonly_background_color=sg.theme_background_color(),
            disabled_readonly_text_color=sg.theme_text_color(),
            border_width=0,
        ),
    ],
    [
        sg.Text(
            "Title: \nDate: \nParodies: \nCharacters: \nTags: \nArtists: \nPages:",
            key="-OUTPUT-",
            enable_events=True,
            expand_y=True,
            s=(50, None),
        ),
        sg.Image(
            key="-IMAGE-",
            size=(210, 300),
            background_color="Black",
            visible=False,
            enable_events=True,
        ),
    ],
]


def format_tags(tags, excluded_tags, pages, language):
    query_string = ""
    tags = tags.split(",")
    excluded_tags = excluded_tags.split(",")

    for tag in tags:
        if tag == "":
            tags.remove("")
    for idx, tag in enumerate(tags):
        if tag[0].isspace():
            tag = tag[1:]
            tag = '"' + tag + '"'
            tags[idx] = tag
        else:
            tag = '"' + tag + '"'
            tags[idx] = tag

    for etag in excluded_tags:
        if etag == "":
            excluded_tags.remove("")
    if excluded_tags != None or False:
        for idx, etag in enumerate(excluded_tags):
            try:
                if etag[0].isspace():
                    etag = etag[1:]
                    etag = '-"' + etag + '"'
                    excluded_tags[idx] = etag
                else:
                    etag = '-"' + etag + '"'
                    excluded_tags[idx] = etag
            except IndexError:
                excluded_tags == None
    full_tags = tags + excluded_tags

    for tag in full_tags:
        query_string = query_string + tag + " "
    if language or language != None or language != "Dont Care":
        query_string = query_string + " language:{}".format(language)
    if pages or pages != 0:
        query_string = query_string + " pages:<={}".format(pages)
    return query_string


def start_search(query_string):
    try:
        results = Utils.search_all_by_query(
            query_string,
            sort=Sort.PopularWeek,
        )
        return list(results)

    except:
        return "nothing found sorry. Check if tags are typed correct"


def get_img_data(f, maxsize=(800, 640), first=False):
    """Generate image data using PIL"""
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


window = sg.Window("Random Doujin", layout, finalize=True, auto_size_text=True)

search_string2 = ""
while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-COVER-" and values["-COVER-"]:
        window["-IMAGE-"].update(visible=True)
    elif event == "-COVER-" and values["-COVER-"] != True:
        window["-IMAGE-"].update(visible=False)
    if event == "-SEARCH-" and values["-TAGS-"] != "":
        tags = values["-TAGS-"]
        etags = values["-ETAGS-"]
        lang = values["-LANG-"]
        pages = values["-PAGES-"]
        search_string = format_tags(tags, etags, pages, lang)
        window["-QUERY-"].update("Search: " + search_string)
        if search_string != search_string2:
            results = start_search(search_string)
        search_string2 = format_tags(tags, etags, pages, lang)
        try:
            result = random.choice(results)
            window["-RESULTS-"].update(" // Results: " + str(len(results)))
            cover = None
            cover = requests.get(result.cover, stream=True)
            cover_data = get_img_data(cover.raw, first=True)
            window["-URL-"].update(result.url)
            window["-IMAGE-"].update(data=cover_data)
            window["-OUTPUT-"].update(
                "Title: {}\nDate: {}\nParodies: {}\nCharacters: {}\nTags: {}\nArtists: {}\nPages: {}".format(
                    result.title(),
                    result.upload_date.strftime("%d.%m.%Y"),
                    Tag.get(result.parody, property_="name"),
                    Tag.get(result.character, property_="name"),
                    Tag.get(result.tag, property_="name"),
                    Tag.get(result.artist, property_="name"),
                    result.num_pages,
                ),
            )

        except IndexError:
            window["-URL-"].update("Sorry Nothing found with this Search")
            window["-OUTPUT-"].update("Title: " + "\n" + "Upload Date: ")
    elif values["-TAGS-"] == "" and event == ["-SEARCH-"]:
        window["-URL-"].update("Tags Can't be empty. Sorry.")
        window["-OUTPUT-"].update("Title: " + "\n" + "Date: ")
    if event == "-OUTPUT-" or event == "-IMAGE-":
        try:
            webbrowser.open_new_tab(result.url)
        except NameError:
            pass


window.close()
