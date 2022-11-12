from htmltools.tags import style, sub
from shiny import App, render, ui
import pandas as pd
import seaborn as sns

sns.set_theme()
# TODO - Refactor: separar datos, ui y server en packages

rankings_df = pd.read_excel("./data/Rankings.xlsx")

# Opciones 
opts_rankings = rankings_df["Ranking"].unique().tolist()
opts_years = rankings_df["Año"].unique().tolist()
opts_instituciones = rankings_df["Institucion"].unique().tolist()
opts_area = rankings_df["Area"].unique().tolist()
opts_subarea = ()
opts_indicador = rankings_df["Indicador"].unique().tolist()

# -----------------------------------------------------------------------------
# Interfaz Gráfica
# -----------------------------------------------------------------------------
app_ui = ui.page_fluid(
    ui.div(
        ui.h1("Tarea 1 - Taller de Aplicaciones 2"),
        ui.p("Integrantes: Ari Romero Garrido - Karen Romero Garrido"),
        ui.p("En este trabajo vamos a realizar un trabajo")
    ),

    ui.navset_tab(
        ui.nav("Explorar Datos", 
            ui.row(
                ui.column(2, 
                    ui.input_selectize(
                        "rankings",
                        "Rankings",
                        opts_rankings,
                        multiple=True
                    ),
                ),
                ui.column(2,
                    ui.input_selectize(
                        "instituciones",
                        "Instituciones",
                        opts_instituciones,
                        multiple=True
                    ),
                ),
                ui.column(2, 
                    ui.input_selectize(
                        "area",
                        "Área",
                        opts_area,
                        multiple=True
                    ),
                ),
                ui.column(2,
                    ui.output_ui("select_subarea"),
                ),
                ui.column(2,
                    ui.input_selectize(
                        "indicador",
                        "Indicador",
                        opts_indicador,
                        multiple=True
                    ),
                ),
            ),
            ui.hr(),
            ui.output_table("df")
        ),
        ui.nav("Ranking por Area", 
            ui.h3("Ranking 1"),
            ui.output_plot("ranking1_plot"),
            ui.h3("Ranking 2"),
            ui.output_plot("ranking2_plot"),
            ui.h3("Ranking 3"),
            ui.output_plot("ranking3_plot"),
        ),
        ui.nav("Ranking por Indicador", 
            "Contenido 1"
        ),
    )
)

# -----------------------------------------------------------------------------
# Servidor 
# -----------------------------------------------------------------------------
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

    @output
    @render.plot(alt="Ranking 1")
    def ranking1_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 1",))
        sub_df = rankings_df[indx_ranking]
        sub_df['Institucion'] = sub_df['Institucion'].str.replace('Universidad ', 'U')
        group_df = sub_df.groupby(
            ["Año", "Institucion", "Area" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.relplot(
            data=group_df,
            x="Institucion", y="Ranking", col="Año",
            hue="Area", style="Area" 
        )

    @output
    @render.plot(alt="Ranking 2")
    def ranking2_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 2",))
        sub_df = rankings_df[indx_ranking]
        sub_df['Institucion'] = sub_df['Institucion'].str.replace('Universidad ', 'U')
        group_df = sub_df.groupby(
            ["Año", "Institucion", "Area" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.relplot(
            data=group_df,
            x="Institucion", y="Ranking", col="Año",
            hue="Area", style="Area" 
        )

    @output
    @render.plot(alt="Ranking 3")
    def ranking3_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 3",))
        sub_df = rankings_df[indx_ranking]
        sub_df['Institucion'] = sub_df['Institucion'].str.replace('Universidad ', 'U')
        group_df = sub_df.groupby(
            ["Año", "Institucion", "Area" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.relplot(
            data=group_df,
            x="Institucion", y="Ranking", col="Año",
            hue="Area", style="Area" 
        )


app = App(app_ui, server)
