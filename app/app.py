from htmltools.tags import style, sub
from shiny import App, render, ui
import pandas as pd
import seaborn as sns

# TODO - Refactor: separar datos, ui y server en packages

rankings_df = pd.read_excel("./data/Rankings.xlsx").dropna()
opts_rankings = rankings_df["Ranking"].unique().tolist()
opts_years = rankings_df["Año"].unique().tolist()
opts_instituciones = rankings_df["Institucion"].unique().tolist()
opts_area = rankings_df["Area"].unique().tolist()
opts_subarea = rankings_df["Subarea"].unique().tolist()
opts_indicador = rankings_df["Indicador"].unique().tolist()

app_ui = ui.page_fluid(
    ui.div(
        children=[
            ui.h1("Tarea 1 - Taller de Aplicaciones 2"),
            ui.p("Integrantes: Ari Romero Garrido - Karen Romero Garrido"),
        ]),
    ui.hr(),
    ui.h2("Exploración de Datos"), ui.navset_tab(
        ui.nav("Exploración Datos", ui.row(
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
                ui.input_selectize(
                    "subarea",
                    "Sub Área",
                    opts_subarea,
                    multiple=True
                ),
            ]),
            ui.column(2, children=[
                ui.input_selectize(
                    "indicador",
                    "Indicador",
                    opts_indicador,
                    multiple=True
                ),
            ]),
        ), ui.output_table("df")),
        ui.nav("Ranking", "Contenido 1"),
        ui.nav("Visualización Por Area", "Contenido 1"),
        ui.nav("Visualización Por Sub Area", "Contenido 1"),
    )
)


def server(input, output, session):
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
