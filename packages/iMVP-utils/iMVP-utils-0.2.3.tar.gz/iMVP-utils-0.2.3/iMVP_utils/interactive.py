import os
import io
from pydoc import classname
from Bio import SeqIO
import time
import iMVP_utils
from iMVP_utils import interactive_functions
# import interactive_functions
import base64
import PIL.Image as Image
import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output,State
from dash import callback_context
from flask import Flask
import plotly.express as px
import plotly.graph_objects as go

def launch_backend(output_path="./output/"):
    """The function to launch the backend for interactive

    Parameters
    ---------
    output_path: str
        The output directory of the files.
    
    Returns
    ---------
        A Dash App object.
    """
    iMVP_finished = False
    input_validated = False
    first_time = True

    assets_path = os.path.dirname(iMVP_utils.__file__) + "/assets/"
    
    server= Flask(__name__)
    app = dash.Dash(name="app1", server=server, assets_folder=assets_path)

    """Run this app with 'python app.py -p port_number and visit http://127.0.0.1:prot_number/ in your web browser.
    (Press CTRL+C to quit)

    """

    if os.path.exists (output_path) == False:
        os.mkdir(output_path)

    def run_iMVP(content, input_parameters):
        """Clustering upload data in fasta format with UMAP and HDBSCAN. 

        Parameters
        ---------
        content: string
            A comma separated string, including type and content of upload file. 
        input_parameters: dict
            A list of reserved parameters for HDBSCAN.
        ---------

        Returns
        ---------
            A Div component: chilren
                A html div of 'processing' information.
            Html stlye: dict
                A style of 'submit-data' button. 
            HDBSCAN_dict: dict
                The results of HDBSCAN.
        """
        nonlocal output_path
        time_start = time.time()
        _, content_string = content.split(',')
        
        decoded = base64.b64decode(content_string)
        style_submit_button = {'width': '40%'}
    
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8').replace("\r\n", "\n").replace("\r", "\n").replace(">", "")),sep = "\n", header=None)
        fa_data = pd.concat([df[::2].reset_index(drop=True),df[1::2].reset_index(drop=True)],axis=1)
        fa_data.columns = ['sites','seq']
        # run HDBSACN
        df_HDBSCAN = interactive_functions.run_cluster(fa_data, output_path, input_parameters)
        
        png = interactive_functions.draw_logo("{path}/init.fa".format(path=output_path), input_parameters)

        image = Image.open(io.BytesIO(png))
        img_file = '{path}/weblogo.png'.format(path=output_path)
        image.save(img_file) 

        HDBSCAN_dict = df_HDBSCAN.to_dict()
        
        time_end = time.time()
        
        
        # used_time = round((time_end - time_start)/60,2)
        used_time = time_end - time_start
        if used_time >= 3600:
            used_time = time.strftime("%H hr %M min %S sec", time.gmtime(used_time))    
        elif used_time >= 60:
            used_time = time.strftime("%M min %S sec", time.gmtime(used_time))   
        else:
            used_time = time.strftime("%S sec", time.gmtime(used_time))   
            
        # except Exception as e :
        #     return html.Div([
        #         'There was an error processing this file.'
        #     ]), {'display':'none'}

        df_groupby = df_HDBSCAN.groupby("Cluster")[["Cluster"]].count()
        df_groupby.columns = ["Count"]
        df_groupby["Cluster ID"] = df_groupby.index
        df_groupby = df_groupby[["Cluster ID", "Count"]]
        print(df_groupby)

        # html.Div([
        #     dash.dash_table.DataTable(df_groupby.to_dict('records'), [{"name": i, "id": i} for i in df_groupby.columns])
        # ], style={"width": "400px", "margin-left":"50px"}
        # ),

        return html.Div([html.H3("{} inputs were analyzed. Finished in {}!".format(df_HDBSCAN.shape[0], used_time)), html.H3('Done!'),]), \
        style_submit_button , HDBSCAN_dict

    def check_fasta_input(content):
        basespace = {i:1 for i in "ATCGUNRDEQHILKMFPSWYV"}
        _, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        N = 0
        is_fasta = True
        try:
            for line in decoded.decode('utf-8').replace("\r\n", "\n").replace("\r", "\n").split("\n"):
                try:
                    # print(line)
                    if not line:
                        continue
                    elif N % 2 == 0:
                        if line.startswith(">") == False:
                            is_fasta = False
                            break
                    elif N % 2 == 1:
                        for b in line:
                            if b.upper() not in basespace:
                                is_fasta = False
                                break
                    N += 1
                except Exception as e:
                    is_fasta = False
                    break
        except Exception as e:
            is_fasta = False
        return is_fasta

    @app.callback(
        Output('upload_data','children'),
        Input('upload_data','filename'),
        State('upload_data', 'contents')
    )

    def upload_info(filenames, contents):
        nonlocal input_validated
        input_validated = False
        if filenames is None:
            return html.Div([
                'Drag and Drop or ',html.A('Click to upload your FASTA file here')
            ], style={"line-height": "300px", "width": "600px"}) #  style={"padding":"50px"}
        else:
            for file, c in zip(filenames, contents):
                fasta_status = check_fasta_input(c)
                if fasta_status == True:
                    input_validated = True
                    return html.Div([html.B('{filename}'.format(filename = file),style={'color':'#ff4777'}),' has been uploaded'], style={"line-height": "300px", "width": "600px"})
                else:
                    return html.Div([html.B('Warining: {filename} is not a validated FASTA file!'.format(filename = file),style={'color':'#ff4777'}),], style={"line-height": "300px", "width": "600px"})
    @app.callback(
                Output('hdbscan-parameter-list','data'),
                Output('processing_1', 'children'),
                Output('processing_3','children'),
                Output('upload_data', 'style'),
                Output('para-list-div', 'style'),
                Output('upload-div', 'style'),
                Input('submit-button-state', 'n_clicks'),
                [
                State('upload_data', 'contents'), 
                State('exp_len', 'value'), 
                State('n_neighbors', 'value'), 
                State('min_dist', 'value'), 
                State('random_state', 'value'), 
                State('umap_jobs', 'value'), 
                State('umap_init', 'value'), 
                State('densmap', 'value'), 
                State('min_cluster_size', 'value'),
                State('min_samples', 'value'),
                State('cluster_selection_method', 'value'),
                State('cluster_selection_epsilon', 'value'),
                State('hdbscan_jobs', 'value'),
                State('softclustering', 'value'),
                State('weblogo_unit', 'value'),
                State('weblogo_first_index', 'value'),
                State('weblogo_base_type', 'value'),
                ],
                prevent_initial_call=True) 

    def infomation_hide_div(n_clicks,list_of_contents, exp_len, n_neighbors, min_dist, random_state, umap_jobs, umap_init, densmap ,min_cluster_size, min_samples, cluster_selection_method, cluster_selection_epsilon, hdbscan_jobs, softclustering, weblogo_unit, weblogo_first_index, weblogo_base_type):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger the clustering.
            list_of_contents: list
                Contents of upload data.
            exp_len: int
                The expected lengths for the sequences.
            n_neighbors: int
                n_neighbors for UMAP.
            min_dist: int
                min_dist for UMAP.
            random_state: int
                random_state for UMAP.
            umap_jobs: int
                n_jobs for UMAP.
            umap_init: str
                init for UMAP.
            densmap: boolean
                densmap for UMAP.
            min_cluster_size: int
                The parameter of HBDSACN from user.
            min_samples: int
                The parameter of HBDSACN from user.
            cluster_selection_method: string
                The parameter of HBDSACN from user.
            core_dist_n_jobs: int
                The parameter of HBDSACN from user.
            softclustering: bool
                The parameter of HBDSACN from user.
            weblog_unit: str
                The parameter for Weblogo.
            weblog_first_index: str
                The parameter for Weblogo.
        ---------

        Return
        ---------
            hdbscan-parameter-list: dict
                The parameters of HDBSCAN from user.
            processing_1: div object
                The information about data processing.
            processing_3: div object
                The information about data processing.
            upload_data: dict
                A Div style of 'upload_data' to hide the div object.
            para-list-div: dict
                A Div style of 'para-list-div' to hide the div.
            upload-div: dict
                A Div style of 'upload-div' to hide the div.
        """
        nonlocal input_validated

        dict_parameters = {
            "exp_len": exp_len,
            "n_neighbors": n_neighbors,
            "min_dist": min_dist,
            "random_state": random_state,
            "umap_jobs": umap_jobs,
            "umap_init": umap_init,
            "densmap": densmap,
            "min_cluster_size": min_cluster_size,
            "min_samples": min_samples,
            "cluster_selection_method": cluster_selection_method,
            "cluster_selection_epsilon": cluster_selection_epsilon,
            "hdbscan_jobs": hdbscan_jobs,
            "softclustering": softclustering,
            "weblogo_unit": weblogo_unit,
            "weblogo_first_index": weblogo_first_index,
            "weblogo_base_type": weblogo_base_type,
        }
        
        if input_validated == True:
            hide_div_style_1 = {'display': 'none'}
            hide_div_style_2 = {'display': 'none'}
            hide_div_style_3 = {'display': 'none'}
            if list_of_contents is not None:
                for c in list_of_contents:
                    return dict_parameters, [html.H3(time.asctime( time.localtime(time.time())))],html.H3('Processing ......',id='process'),hide_div_style_1,hide_div_style_2,hide_div_style_3
        else:
            return dash.no_update

    @app.callback(
                Output('processing_2', 'children'),
                Output('submit-data', 'style'),
                Output('cluster-data', 'data'),
                Output('processing_3','style'),
                Output('horizontal_line','style'),
                Input('hdbscan-parameter-list','data'),
            [State('upload_data', 'contents')],
                prevent_initial_call=True)

    def upload_file(parameter_list, list_of_contents):

        """
        Parameters
        ---------
            parameter_list: list
                The parameters of HDBSCAN from user.
            list_of_contents: list
                A content of upload file.

        ---------

        Returns
        ---------
            processing_2: div object
                The information about data processing.
            style: dict
                A style to hide 'submit-data' div object.
            parameters_dict: dict
                The results of clustering with HDBSCAN. 
            hide_info_style: dict
                A style to hide 'processing_2' div object.
            display_hr: dict
                A style to display horizontal line.
        """  
        nonlocal iMVP_finished

        hide_info_style  = {'display':'none'}
        display_hr = {'display':'inline-block'}

        if list_of_contents is not None:
            for c in list_of_contents:
                iMVP_out =  run_iMVP(c, parameter_list)
                if len(iMVP_out) == 2:
                    processing_2, style = iMVP_out
                    parameters_dict = None
                else:
                    processing_2, style, parameters_dict = iMVP_out
                    iMVP_finished = True
        return processing_2, style, parameters_dict, hide_info_style, display_hr


    @app.callback(
        Output('cluster_figure', 'figure'),
        Output('my-checklist','options'),
        Output('type', 'data'),
        Output('hidden_data','style'),
        Output('submit-button','style'),
        [Input('submit-data','n_clicks'),
        State('cluster-data', 'data'),
        Input("scatter-slider", "value"), 
        ],prevent_initial_call=True
    )

    def cluster_figure(n_clicks, cluster_data, markersize):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger clustering.
            cluster_data: dict
                The results of clustering with HDBSCAN.
            markersize:
                The size of markers
        ---------

        Returns
        ---------
            cluster_figure:  graph object in plotly
                A graph to display the clusters of HBDSCAN.
            my-checklist: list
                The types of cluster that user choosed.
            type: list
                Types of clusters.
            hidden_data: dict
                A style to hide the div object.
            submit-button: button object
                A style to show the div of button object. 

        """
        dff = pd.DataFrame(cluster_data)
        df = dff.sort_values(by="Cluster", ascending=True)
        type = range(1,max(df['Cluster']) + 1)
        df['Cluster'] = df['Cluster'].astype(str)
        available_type =  list(map(str, type)) 
        df['customdata'] = df.index.values.tolist()
        options = [{'label': '{:>3}'.format(i), 'value':i } for i in available_type]
        fig = px.scatter(df, x="X", y="Y", color="Cluster", custom_data=["customdata"])
        fig.update_traces(marker_size=markersize) # , selector=dict(mode='markers')
        fig.update_layout(dragmode='lasso', hovermode=False, width=600, height=600)
        
        return fig, options,available_type,{'display':'inline-block', 'min-width': "1200px"},{'display':'none'} # 

    @app.callback(
        Output("my-checklist", "value"),
        Output("all-or-none", "value"),
        Output("select-data","data"),
        [Input("type", 'data'),
        Input("all-or-none", "value"),
        Input("my-checklist", 'value')],
    )

    def select_all_none(option,all_selected, my_selected):
        """
        Parameters
        ---------
            option: list
                Types of all clusters.
            all_selected: list
                When user choose all clusters. 
            my_selected: list 
                Types of clusters that user choosed.

        ---------

        Returns
        ---------
            my-checklist: list
                Types of clusters that user choosed, which show as checklist object.
            all-or-none: list
                Types of all clusters, which show as checklist object.
            select-data: list
                Types of clusters that user choosed, which store as dcc object.

        """
        ctx = callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if input_id == "my-checklist":
            all_selected = ["Select All"] if set(my_selected) == set(option) else []
        else:
            my_selected = option if all_selected else []
        if all_selected != []:
            select_data = option
        else:
            select_data = my_selected

        return my_selected, all_selected, select_data

    @app.callback(
        Output('weblogo','src'),
        Input('cluster_figure', 'selectedData'),
        Input('cluster-data', 'data'),
        Input('select-data','data'),
        Input('hdbscan-parameter-list','data'),
        prevent_initial_call=True
        )

    def draw_weblogo(selected_data,cluster_data, clusters_select, parameter_list):
        """
        Parameters
        ---------
            selected_data: dict
                Data selected with lasso or checklist
            cluster_data: dict
                The results of clustering with HDBSCAN. 
            clusters_select: list 
                Types of clusters selected from users
        ---------

        Return
        ---------
            weblogo: png
                Weblogo picture in png format.
        ---------
        """
        nonlocal output_path, iMVP_finished, first_time
        if iMVP_finished == True and first_time == True:
            # and os.path.isfile("{path}/selected_data.fa".format(path=output_path)) == False
            img_file = '{path}/weblogo.png'.format(path=output_path)
            encode_img = base64.b64encode(open(img_file,'rb').read())
            iMVP_finished = True
            first_time = False
            return 'data:image/png;base64,{}'.format(encode_img.decode())
        elif clusters_select == [] and selected_data is None:
            return dash.no_update
        else:
            df = pd.DataFrame(cluster_data)
            df['Cluster'] = df['Cluster'].astype(str)
            fa_index = []
            if selected_data is None:
                custom = []
                selected_data = {}
                for i in df[df['Cluster'].isin(clusters_select) ].index.values.tolist():
                    custom.append({'customdata':[i]})
                selected_data['points'] = custom
            
            for points in selected_data['points']: 
                fa_index.extend(points.get('customdata'))
            
            fasta_name = "{path}/selected_data.fa".format(path=output_path)

            base_type = parameter_list["weblogo_base_type"]

            with open(fasta_name, "w") as fasta_out:
                for idx, row in df.loc[fa_index].iterrows():
                    if base_type == "DNA":
                        seq_out = str(row["seq"]).upper().replace("U", "T")
                    elif base_type == "RNA":
                        seq_out = str(row["seq"]).upper().replace("T", "U")
                    else:
                        seq_out = str(row["seq"])
                    fasta_out.write(">{}\n{}\n".format(idx, seq_out))

            png = interactive_functions.draw_logo(fasta_name, parameter_list)
            image = Image.open(io.BytesIO(png))
            img_file = '{path}/weblogo.png'.format(path=output_path)
            image.save(img_file) 
            encode_img = base64.b64encode(open(img_file,'rb').read())
            
            return 'data:image/png;base64,{}'.format(encode_img.decode())

    @app.callback(
        Output("download-text", "data"),
        Input("btn-download-txt", "n_clicks"),
        prevent_initial_call=True)
    def download_fasta(n_clicks):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger download file in fasta format.
        ---------

        Return
        ---------
            download-text: string   
                A fasta format file.
        ---------
        """
        nonlocal output_path
        with open('{path}/selected_data.fa'.format(path=output_path)) as f:
            contents = f.read()
        return dict(content=contents, filename="seleted_data.fa")

    @app.callback(
        Output("download-csv", "data"),
        Input("btn-download-csv", "n_clicks"),
        prevent_initial_call=True)
    def download_csv(n_clicks):
        """
        Parameters
        ---------
            n_clicks: int
                The number of clicks to trigger download CSV file.
        ---------

        Return
        ---------
            download-text: string   
                A fasta format file.
        ---------
        """
        nonlocal output_path
        with open('{path}/all_clusters.csv'.format(path=output_path)) as f:
            contents = f.read()
        return dict(content=contents, filename="all_clusters.csv")

    @app.callback(
        Output("download-png", "data"),   
        Input("btn-download-png", "n_clicks"),
        prevent_initial_call=True
    )
    def download_weblogo(n_clicks):
        nonlocal output_path
        """
        Parameters
        ---------
            n_clicks: int 
                The number of clicks to trigger download weblogo picture.
        ---------

        Return
        ---------
            download-png: png
                A file in png format of weblogo.
        ---------
        """
        return dash.dcc.send_file("{path}/weblogo.png".format(path=output_path))

    app.layout = html.Div([



        html.Div([
            html.Div([
                html.H1(
                        "iMVP Motif Viewer",
                        style = {'textAlign':'center'}), # , 'margin-left':'20%'

                html.H3(
                        "Version: 0.2.3; Contributed by Jing Yao, Jianheng Liu @ Zhang Lab (SYSU).",
                        style = {'textAlign':'center'}), # , 'margin-left': '10%'
                html.H3("Documents: https://readthedocs.org/iMVP/", style = {'textAlign':'center'}),

                html.Div([
                    # html.Br(),
                    # html.Br(),
                    html.Div("Tips #1: To go back to the parameters page, please refresh the page."),
                    html.Div("Tips #2: Use Ctrl+C in command lines to terminate the backend."),
                ], style={"horizonal-align":"center", 'text-align':'center'}),
            ], style={"width":"1000px"}),

            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H4('I. Upload data'),
                                dcc.Upload(
                                    id = 'upload_data',
                                    multiple=True,
                                    style={"line-height": "300px"}  # , "min-width": "100%
                                ), 

                            ], className = "upload",id = 'upload-div', style={'display':'inline-block', "width": "600px"},  # "line-height: 20%;"
                            ),

                        html.Div([
                                html.Br(),
                                html.Br(),
                                html.Div("If you have confirmed your input and parameters, click the button to run."),
                                html.Br(),
                                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                            ],
                            className="input", style={"horizonal-align":"center", 'text-align':'center'},
                        ),

                    ], className="two columns", style={'display':'inline-block', "width": "600px", "vertical-align":"top", "margin-right":"5%", "margin-left":"2.5%"}
                    ),

                    # html.Div([

                    #     ], className="three columns", style={'display':'inline-block'}
                    # ),

                    html.Div([
                        html.Div([
                            html.H4('II. Quality control'),
                            html.Div([
                                "1. Expected lengths of the sequences =",
                                dcc.Input(id='exp_len', type='number', value='21', min='0'),
                            ]),
                            ], style={'display':'inline-block', "vertical-align":"top"}),

                            html.H4('III. UMAP parameters'),
                            html.Div([
                                "1. n_neighbors =",
                                dcc.Input(id='n_neighbors', type='number', value='20', min='0'),
                                ]),
                            html.Div([
                                "2. min_dist =", 
                                dcc.Input(id='min_dist', type='number', value='0.01', step='any', min='0', max='1'), 
                                ]),
                            html.Div([
                                "3. random_state =", 
                                dcc.Input(id='random_state', type='number', value='42', min='-2147483648', max='2147483647'), 
                                ]),
                            html.Div([
                                "4. jobs =", 
                                dcc.Input(id='umap_jobs', type='number', value='6'), 
                                ]),
                            html.Div([
                                html.Div(["5. init ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['random', 'spectral'], 'random', id='umap_init')], className="two columns", style={"display": "inline-block"}),        
                            ], className="row"# style={"width":"30%"}
                            ),
                            html.Div([
                                html.Div(["6. DensMAP ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['True', 'False'], 'False', id='densmap')], className="two columns", style={"display": "inline-block"}),        
                            ], className="row"# style={"width":"30%"}
                            ),

                            html.H4('IV. HBDSCAN parameters'),
                            html.Div([
                                "1. min_cluster_size =",
                                dcc.Input(id='min_cluster_size', type='number', value='100'),
                                ]),
                            html.Div([
                                "2. min_samples =", 
                                dcc.Input(id='min_samples', type='number', value='100'),
                                ]),
                            html.Div([
                                "3. cluster_selection_epsilon =", 
                                dcc.Input(id='cluster_selection_epsilon', type='number', step="any", value='0.0'),
                                ]),

                            html.Div([
                                html.Div(["4. cluster_selection_method ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['eom', 'leaf'], 'eom', id='cluster_selection_method')], className="two columns", style={"display": "inline-block"}),        
                            ], className="row"# style={"width":"30%"}
                            ),

                            html.Div([
                                html.Div(["5. soft clustering ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['True', 'False'], 'True', id='softclustering')], className="two columns", style={"display": "inline-block"}),        
                            ], className="row"# style={"width":"30%"}
                            ),
                            html.Div([
                                "6. jobs =", 
                                dcc.Input(id='hdbscan_jobs', type='number', value='6'),
                                ]),

                            html.H4('V. Weblogo'),
                            html.Div([
                                html.Div(["1. Unit ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['probability', 'bits'], 'probability', id='weblogo_unit')], className="two columns", style={"display": "inline-block"}),        
                            ], className="row"# style={"width":"30%"}
                            ),
                            html.Div([
                                html.Div(["2. Base type (LOGO and FASTA output) ="], className="two columns", style={"display": "inline-block"}), # style={"display": "inline-block"}
                                html.Div([dcc.RadioItems(['As input', 'DNA', "RNA"], 'As input', id='weblogo_base_type')], className="two columns", style={"display": "block"}),  # inline-    
                            ], className="row"# style={"width":"30%"}
                            ),

                            html.Div(["3. First index =",
                                        dcc.Input(id='weblogo_first_index', type='number', value='-10'),
                                ]), 
                                
                        ], className="two columns", style={'display':'inline-block'} 
                        ),

                    ], style={'display':'inline-block', "margin-left":"0%", "width":"100%"}, # , "width":"40%"
                    ),
                ], className="row", style={'display':'inline-block', "width":"100%"}
                ),

                        
            ], id="para-list-div", style={"width":"auto"})

        ], className="section1",id = 'section1', style={"width":"1600px"}),

        html.Hr(id = "horizontal_line",style={'display':'none'}),

        html.Div([
            html.Div([
                html.Div([
                    html.Div(
                        dcc.Graph(id = 'cluster_figure'),
                        style={'display': 'inline-block'} # 'width': '40%',
                    ),
                    html.Div(
                        html.H4("Marker size:"),
                        style={"margin-left": "10%"}
                    ),
                    html.Div(
                            dcc.Slider(id='scatter-slider', value=10, min=1, max=30,),
                            style={"margin-left": "10%", "margin-right": "10%"}
                    ), 

                ], className="two columns", style={"min-width":"600px", "display": "inline-block", "max-width": "40%", "margin-right": "5%"} # , "margin-right": "%"
                ),

                html.Div([
                    html.Div([
                        html.Div(
                            html.Img(id = "weblogo", style={'max-width':"600px",'display': 'inline-block'}), 
                            style={'display': 'inline-block'}   # , 'verticalAlign':'top'
                            ), 
                            # style={'width':"200px"}), # 'width': '50%','display': 'inline-block', 'position':'relative','bottom':'150px'

                    html.Div([
                        html.Div([
                            html.Div(html.Button("Download FASTA", id = "btn-download-txt"), # , style = {'width': '99%'}
                            ),
                            dcc.Download(id = "download-text")
                        ],
                        style={'display':'inline-block', "margin-left": "10%", "margin-right":"5%"}, 
                        className='three columns'), 

                        html.Div([
                            html.Div(html.Button("Download CSV", id="btn-download-csv"), # , style={'width': '99%'}
                            ),
                            dcc.Download(id = "download-csv"),
                        ],
                        style={'display':'inline-block', "margin-left":"5%", "margin-right":"5%"}, 
                        className='three columns'),

                        html.Div([
                            html.Div(html.Button("Download LOGO", id="btn-download-png"), # , style={'width': '99%'}
                            ),
                            dcc.Download(id = "download-png"),
                        ],
                        style={'display':'inline-block', "margin-left":"5%", "margin-right": "10%"}, 
                        className='three columns'),

                    ], className="row", style={"horizonal-align": "middle", "margin-left": "5%", "margin-top": "5%", "margin-right": "5%", "margin-bottom": "5%"} # 'display': 'inline-block', 
                    ),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        html.Div(
                            html.H4("Select clusters:", style={'display': 'inline-block'}),
                        ),
                        
                        html.Div([
                            dcc.Checklist(
                                id="all-or-none",
                                options=[{"label": "Select All", "value": "Select All"}],
                                value=[],
                                # labelStyle={"display": "inline-block", "position": "relative", "vertical-align":"middle"},
                            ),
                        ],  # style={'display': 'inline-block'}
                        ),

                        html.Div([
                            dcc.Checklist(
                                id="my-checklist",
                                #options=[{"label": x, "value": x} for x in option],
                                value=["1"],
                                # labelStyle={"display": "inline-block", "position": "relative", "vertical-align":"middle"}, # "text-": "relative"
                            ),
                        ], # style={'display': 'inline-block'}
                        ),
                    ], style={'display': 'inline-block'}),

                    ], style={'display': 'inline-block'}
                    ),

                ], className="two columns", style={"margin-top":"5%", "max-width": "40%", "display": "inline-block",'vertical-align': 'top'} 
                ),
            ], className="row", style={"display": "inline-block", "min-width":"1000px"} 
            ),
            html.Br(),
            html.Br(),
            html.Br(),

        ], id = "hidden_data", style={'display':'none', 'min-width': '1000px'},
        ),

        

        # html.Div(
        #     dcc.Markdown('''
        #         *Usage:*
        #             The software encodes the data using one-hot encoding and the dimensionality reduction using **UMAP**. Then, the matrix is clustered using **HDBSCAN** to get all the clusters from the fasta file.Firstly, upload the fasta data of the same length. Then, input the parameters for the clustering with HDBSCAN. After submitting the data, it will take a few minutes for the background to process the data.Finally, you can select clusters by tick checklist, or use a lasso to circle the parts of interest on the cluster plot. That part of data would display by weblogo of base enrichment.
        #         ''')
        # )

        html.Div(id = "processing_1"),
        html.Div(id = "processing_2"),
        html.Div(id = "processing_3"),
        html.Div(
            html.Button(
                    id = 'submit-data',
                    n_clicks=0,
                    children='Draw the Figures',
                    style = {'display':'none'}),
            id = 'submit-button'),

        dcc.Store(id = "cluster-data"),
        dcc.Store(id = "hdbscan-parameter-list"),
        dcc.Store(id = "select-data"),
        dcc.Store(id = "type")
    
    ], style={"margin-left":"0%", "width":"1000px"})

    return app

if __name__ == "__main__":
    pass