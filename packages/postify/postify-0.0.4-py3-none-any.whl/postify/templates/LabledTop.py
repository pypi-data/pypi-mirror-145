from .. import Color, Cache, Border, Line, Text

def LabledTop ( text_large = "", text_small_1 = "", text_small_2 = "" ):

    Border.Rounded(radius=0.01, color=Color.white)

    Border.Head(size=0.22, color=Color.white, resize=True)
    Line.Horizontal(color=Color.black, height=0.09, thickness=0.002)
    Text.RightAlign(text=text_large, font=Text.Fonts['Jura'], size=0.07, x=1, color=Color.black, y=0.057)
    Text.LeftAlign(text=text_small_1, font=Text.Fonts['Jura'], size=0.03, color=Color.black, y=0.11, x=0.005)
    Text.RightAlign(text=text_small_2, font=Text.Fonts['Jura'], size=0.03, color=Color.black, y=0.11, x=0.995)

    Border.Even(size=0.05, resize=True, color=Color.white)

