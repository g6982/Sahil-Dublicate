# -*- coding: utf-8 -*-

{
    "name": "Inventory mobile barcode/QR code scanner | Receipts Internal Transfers and Delivery Orders | Inventory Adjustment | Scrap Order | Stock Replenishment | Lot/Serial Number | Stock Location",
    "version":"15.0.1",
    "license": "OPL-1",
    "support": "relief.4technologies@gmail.com",  
    "author" : "Relief Technologies",    
    "category": "Inventory/Inventory",
    "summary": "stock barcode inventory barcode mobile barcode scan mobile qr code scan all in one mobile qr scanner all in one mobile barcode scanner mobile camera inventory adjustment barcode stock adjustment barcode stock picking barcode scrap barcode qrcode scan",
    "description": """

    """,
    "depends": [
        "rt_widget_qr_cam",
        "stock"
    ],
    "data": [
        "views/stock_picking.xml",
        "views/stock_move.xml",
        "views/stock_orderpoint.xml",
        "views/stock_quant.xml",
        "views/stock_scrap.xml",
        "views/stock_production_lot.xml",
        "views/stock_location.xml",
    ],
     
    "images": ["static/description/background.png",],              
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 4,
    "currency": "EUR"   
}
