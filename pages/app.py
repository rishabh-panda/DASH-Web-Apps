from turtle import width
from dash import Dash, html, dcc
import dash
import base64

background_image = "./Assets/background_image.png"
background_image_base64 = base64.b64encode(open(background_image, 'rb').read()).decode('ascii')

navigation_logo = "./Assets/ma_navigation.png"
navigation_logo_base64 = base64.b64encode(open(navigation_logo, 'rb').read()).decode('ascii')

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                html.Img(src='data:image/png;base64,{}'.format(navigation_logo_base64),
                         style={'width': '350px',
                                'height': 'auto',
                                'position': 'absolute', 
                                'margin-top': '100px',
                                'margin-left': '40px'})
            ),
            html.Div([
                
                 html.Div(
                [
                    html.Div(
                        "Point of departure",
                        style={
                            "color":"rgb(204,0,0)",
                            'font-size':'25px',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        "Portfolio overview",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Monday morning report",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Results tracking",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Category overview",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Category roles",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Store overview",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Category diagnostic",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Category market diagnostic",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Category performance score card",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    
                    html.Div(
                        [
                            html.Div(
                                "Customer decision tree",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Merchandizing levers",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        )
                    ],
                 style={'flex': 1, 'margin':'0.7rem', 'height': '850px', 'width':'320px','background':'white','padding':'0.7rem'}
            ),


          html.Div(
                [
                    html.Div(
                        "Assortment planning",
                        style={
                            "color":"rgb(204,0,0)",
                            'font-size':'25px',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        "Assortment performance",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Market segment priorities",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Assortment efficiency",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Loyalty and substitution",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Assortment decisions",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Price pack architecture",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    dcc.Link(
                        html.Div(
                            [
                                html.Div(
                                    "Assortment optimization",
                                    style={
                                        'font-family': 'Arial',
                                        'margin-bottom': '20px'
                                    }
                                ),
                                html.Div(
                                    "❯",
                                    style={
                                        "color": "rgb(204,0,0)",
                                        'font-size': '15px',
                                        'margin-left': 'auto'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                'flex-direction': 'row'
                            }
                        ),
                        href='http://127.0.0.1:8050/assortment-optmimization-dashboard',
                        style={'text-decoration': 'none'},
                        target='_blank'
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Assortment additions",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Store clustering and localization",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Distribution",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Planning review",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px",
                            'font-weight':'bold',
                            }
                        ),
                    dcc.Link(
                        html.Div(
                            [
                                html.Div(
                                    "Scenario modeling",
                                    style={
                                        'font-family': 'Arial',
                                        'margin-bottom': '20px'
                                    }
                                ),
                                html.Div(
                                    "❯",
                                    style={
                                        "color": "rgb(204,0,0)",
                                        'font-size': '15px',
                                        'margin-left': 'auto'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                'flex-direction': 'row'
                            }
                        ),
                        href='http://127.0.0.1:8050/scenario-modeling-dashboard',
                        style={'text-decoration': 'none'},
                        target='_blank'
                    ),
                    dcc.Link(
                        html.Div(
                            [
                                html.Div(
                                    "Category plan",
                                    style={
                                        'font-family': 'Arial',
                                        'margin-bottom': '20px'
                                    }
                                ),
                                html.Div(
                                    "❯",
                                    style={
                                        "color": "rgb(204,0,0)",
                                        'font-size': '15px',
                                        'margin-left': 'auto'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                'flex-direction': 'row'
                            }
                        ),
                        href='http://127.0.0.1:8050/category-plan-dashboard',
                        style={'text-decoration': 'none'},
                        target='_blank'
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Micro space planning",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Space optimization",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    ],
                 style={'flex': 1, 'margin':'0.7rem', 'height': '850px', 'width':'320px','background':'white','padding':'0.7rem'}
            ),

           html.Div(
                [
                    html.Div(
                        "Supplier negotiations",
                        style={
                            "color":"rgb(204,0,0)",
                            'font-size':'25px',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        "Negotiation summary",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Supplier landscape",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Supplier summary",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "First as...",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Supplier negotiation levers",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        "Financial overview:",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Sub-category",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Supplier",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "It...",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    dcc.Link(
                        html.Div(
                            [
                                html.Div(
                                    "Market overview",
                                    style={
                                        'font-family': 'Arial',
                                        'margin-bottom': '20px'
                                    }
                                ),
                                html.Div(
                                    "❯",
                                    style={
                                        "color": "rgb(204,0,0)",
                                        'font-size': '15px',
                                        'margin-left': 'auto'
                                    }
                                )
                            ],
                            style={
                                'display': 'flex',
                                'flex-direction': 'row'
                            }
                        ),
                        href='http://127.0.0.1:8050/market-overview-dashboard',
                        style={'text-decoration': 'none'},
                        target='_blank'
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Supplier operations",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Space profitability",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Payment terms",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Competitive pricing",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Promotions contributions",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Input cost module",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px",
                            'font-weight':'bold',
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Risk and opportunity",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Commodity level exposure",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Negotiation opportunities",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Item pricing impact",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Commodity pricing trend",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    ],
                 style={'flex': 1, 'margin':'0.7rem', 'height': '850px', 'width':'320px','background':'white','padding':'0.7rem'}
            ),

            html.Div(
                [
                    html.Div(
                        "Pricing and promotions",
                        style={
                            "color":"rgb(204,0,0)",
                            'font-size':'25px',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        "Pricing accelerator",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "KVI classification",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Competitor matching",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Price setting",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Reporting",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        "Promotions accelerator",
                        style={
                            'font-weight':'bold',
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Category analysis",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Sales and margin",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Sales and margin lift",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Promotions list",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    html.Div(
                        [
                            html.Div(
                                "Performance drivers",
                        style={
                            'font-family':'Arial',
                            "margin-bottom": "20px"
                            }),
                            html.Div(
                                "❯",
                                style={
                            "color":"rgb(204,0,0)",
                            'font-size':'15px',
                            'margin-left': 'auto'}
                                )
                            ],
                            style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
                    ],
                 style={'flex': 1, 'margin':'0.7rem', 'height': '850px', 'width':'320px','background':'white','padding':'0.7rem'}
            ),
          
                ],
                     style={
                         'margin-left':'400px',
                         'display':'flex',
                         'margin-top': '100px',
                         }
                   
                     ),
           
           
           
        ],
        style={
            'background-image': f'url(data:image/png;base64,{background_image_base64})',
            'background-size': 'cover',
            'height': '100vh',
            'width':'100%',
            'display':'flex',
            'overflow':'hidden'
        }
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server()
