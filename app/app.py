from htmltools.tags import style, sub
from shiny import App, render, ui
import pandas as pd
import seaborn as sns

sns.set_theme()
# TODO - Refactor: separar datos, ui y server en packages

rankings_df = pd.read_excel("./data/Rankings.xlsx")
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 2', '02')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 3', '03')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 4', '04')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 5', '05')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 6', '06')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 7 ', '07') # 
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 7', '07')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 8', '08')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 9 ', '09') # 
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 9', '09')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 10', '10')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 11', '11')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 12', '12')
rankings_df['Institucion'] = rankings_df['Institucion'].str.replace('Universidad 1', '01')

# Opciones 
opts_rankings = rankings_df["Ranking"].unique().tolist()
opts_years = rankings_df["Año"].unique().tolist()
opts_instituciones = rankings_df["Institucion"].unique().tolist()
opts_area = rankings_df["Area"].unique().tolist()
opts_subarea = ()
opts_indicador = rankings_df["Indicador"].unique().tolist()

print(opts_instituciones)
# -----------------------------------------------------------------------------
# Interfaz Gráfica
# -----------------------------------------------------------------------------
app_ui = ui.page_fluid(
    ui.div(
        ui.h1("Tarea 1 - Taller de Aplicaciones 2"),
        ui.p("Integrantes: Ari Romero Garrido - Karen Romero Garrido"),
    ),

    ui.navset_tab(
        ui.nav("Explorar Datos", 
            ui.p("Esta vista muestra los datos específicos que se muestran gráficamente en las demás pestañas."),
            ui.hr(),
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
            ui.output_table("df")
        ),
        ui.nav("Ranking por Institución", 
            ui.p("Esta vista muestra un detalle del ránking por cada área especfica, separados por año."),
            ui.hr(),
            ui.h3("Ranking 1"),
            ui.output_plot("ranking1_plot"),
            ui.h3("Ranking 2"),
            ui.output_plot("ranking2_plot"),
            ui.h3("Ranking 3"),
            ui.output_plot("ranking3_plot"),
        ),
        ui.nav("Puntaje Por Institución", 
            ui.p("Esta vista muestra el comportamiento gneral de los puntajes de cada institución, separados por ránking."),
            ui.hr(),
            ui.h3("Ranking 1"),
            ui.output_plot("puntaje1_plot"),
            ui.h3("Ranking 2"),
            ui.output_plot("puntaje2_plot"),
            ui.h3("Ranking 3"),
            ui.output_plot("puntaje3_plot"),
        ),
        ui.nav("Ranking por Año", 
            ui.p("Esta vista muestra el comportamiento en el tiempo del ránking de las instituciones."),
            ui.hr(),
            ui.h3("Ranking 1"),
            ui.output_plot("rankinganual1_plot"),
            ui.h3("Ranking 2"),
            ui.output_plot("rankinganual2_plot"),
            ui.h3("Ranking 3"),
            ui.output_plot("rankinganual3_plot"),
        )
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
    @render.plot(alt="Puntaje Institución")
    def puntaje1_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 1",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion","Indicador" ]
        )["Valor indicador (numerico)"].mean().to_frame(name = "Valor").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.boxplot(
            data=group_df,
            x="Institucion", y="Valor"
        )

    @output
    @render.plot(alt="Puntaje Institución")
    def puntaje2_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 2",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion","Indicador" ]
        )["Valor indicador (numerico)"].mean().to_frame(name = "Valor").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.boxplot(
            data=group_df,
            x="Institucion", y="Valor"
        )

    @output
    @render.plot(alt="Puntaje Institución")
    def puntaje3_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 3",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion","Indicador" ]
        )["Valor indicador (numerico)"].mean().to_frame(name = "Valor").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.boxplot(
            data=group_df,
            x="Institucion", y="Valor"
        )

    @output
    @render.plot(alt="Ranking 1")
    def rankinganual1_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 1",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.lineplot(
            data=group_df,
            x="Año", y="Ranking",
            hue="Institucion", style="Institucion"
        )

    @output
    @render.plot(alt="Ranking 2")
    def rankinganual2_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 2",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.lineplot(
            data=group_df,
            x="Año", y="Ranking",
            hue="Institucion", style="Institucion"
        )

    @output
    @render.plot(alt="Ranking 3")
    def rankinganual3_plot():
        indx_ranking = rankings_df["Ranking"].isin(("Ranking 3",))
        sub_df = rankings_df[indx_ranking]
        group_df = sub_df.groupby(
            ["Año", "Institucion" ]
        )["Ranking global"].mean().to_frame(name = "Ranking").reset_index()
        group_df.sort_values(by=["Institucion"], inplace=True)
        return sns.lineplot(
            data=group_df,
            x="Año", y="Ranking",
            hue="Institucion", style="Institucion"
        )

app = App(app_ui, server)
