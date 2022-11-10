from htmltools.tags import style, sub
from shiny import App, render, ui
import pandas as pd
import seaborn as sns

sns.set_theme()
# TODO - Refactor: separar datos, ui y server en packages

rankings_df = pd.read_excel("./data/Rankings.xlsx").dropna()
opts_rankings = rankings_df["Ranking"].unique().tolist()
opts_years = rankings_df["Año"].unique().tolist()
opts_instituciones = rankings_df["Institucion"].unique().tolist()
opts_area = rankings_df["Area"].unique().tolist()
opts_subarea = ()
opts_indicador = rankings_df["Indicador"].unique().tolist()

app_ui = ui.page_fluid(
    ui.div(
    children=[
        ui.h1("Tarea 1 - Taller de Aplicaciones 2"),
        ui.p("Integrantes: Ari Romero Garrido - Karen Romero Garrido"),
    ]),
    ui.row(
        ui.column(2, children=[
            ui.input_selectize(
                "rankings",
                "Rankings",
                opts_rankings,
                multiple=True
            ),
        ]),
        ui.column(2, children=[
            ui.input_selectize(
                "instituciones",
                "Instituciones",
                opts_instituciones,
                multiple=True
            ),
        ]),
        ui.column(2, children=[
            ui.input_selectize(
                "area",
                "Área",
                opts_area,
                multiple=True
            ),
        ]),
        ui.column(2, children=[
            ui.output_ui("select_subarea"),
        ]),
        ui.column(2, children=[
            ui.input_selectize(
                "indicador",
                "Indicador",
                opts_indicador,
                multiple=True
            ),
        ]),
    ),
    ui.hr(),
    ui.navset_tab(
        ui.nav("Explorar", ui.output_table("df")),
        ui.nav("Ranking por Area / Sub Area", "Contenido 1"),
        ui.nav("Ranking por Indicador", "Contenido 1"),
    )
)


def server(input, output, session):

    @output
    @render.ui()
    def select_subarea():
        indx_area = rankings_df["Area"].isin(input.area())
        sub_df = rankings_df[indx_area]
        opts_subarea = sub_df["Subarea"].unique().tolist()
        return ui.input_selectize(
                "subarea",
                "Sub Área",
                opts_subarea,
                multiple=True
            )

    @output
    @render.table
    def df():
        indx_ranking = rankings_df["Ranking"].isin(input.rankings())
        indx_instituciones = rankings_df["Institucion"].isin(input.instituciones())
        indx_area = rankings_df["Area"].isin(input.area())
        indx_subarea = rankings_df["Subarea"].isin(input.subarea())
        indx_indicador = rankings_df["Indicador"].isin(input.indicador())
        sub_df = rankings_df[indx_ranking & indx_instituciones & indx_area & indx_subarea & indx_indicador]
        return sub_df


app = App(app_ui, server)
