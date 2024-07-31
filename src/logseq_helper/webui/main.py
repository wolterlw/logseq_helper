import fasthtml.common as F

app, rt, *_ = F.fast_app(live=True)


@rt("/")
def get():
    return F.Titled("Logseq UI", F.Div(F.P("Hello logseq")))


F.serve()
