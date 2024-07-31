import fasthtml.common as F
from fasthtml import picolink, Style

css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, cursive;}")
app = F.FastHTML(hdrs=(css, picolink))

KNOWN_TAGS = ["12345", "abcde", "random", "stuff", "random123", "1243t45", "absadasd"]


def tag_selection():
    return F.Div(
        F.Group(None, id="selected-tags"),
        F.Form(
            F.Input(id="newtag"),
            hx_post="/tag-search",
            target_id="matched-tags",
            hx_trigger="keyup",
        ),
        F.Div(None, id="matched-tags"),
    )


def results():
    results = F.Ul(id="results")
    return results


@app.get("/")
def get_root():
    return F.Titled("Logseq UI", F.Div(tag_selection(), results()))


def tag_variant(name: str):
    return F.Button(
        name,
        cls="secondary",
        style="width: 100%; border-radius: 0px; text-align: start",
        hx_post=f"/tag-selected/{name}",
        target_id="selected-tags",
        hx_swap="afterend",
    )


@app.post("/tag-selected/{name}")
def tag_selected(name: str):
    return (
        F.Button(
            name, cls="contrast", hx_swap="delete", hx_delete=f"/tag-remove/{name}"
        ),
        F.Div(None, id="matched-tags", hx_swap_oob="true"),
        F.Input(id="newtag", hx_swap_oob="true"),
    )


@app.delete("/tag-remove/{name}")
def tag_removed(name):
    print(f"removing {name}")


@app.post("/tag-search")
def tag_search(newtag: str):
    if not newtag:
        return None
    found = [tag_variant(s) for s in KNOWN_TAGS if s.startswith(newtag)]
    return tuple(found)


@app.get("/item")
def get_item():
    return F.Div("**Hello**", cls="markdown")


F.serve()
