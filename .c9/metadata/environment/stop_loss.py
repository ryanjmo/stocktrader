{"filter":false,"title":"stop_loss.py","tooltip":"/stop_loss.py","undoManager":{"mark":56,"position":56,"stack":[[{"start":{"row":88,"column":109},"end":{"row":88,"column":110},"action":"remove","lines":["e"],"id":224},{"start":{"row":88,"column":108},"end":{"row":88,"column":109},"action":"remove","lines":["s"]},{"start":{"row":88,"column":107},"end":{"row":88,"column":108},"action":"remove","lines":["l"]},{"start":{"row":88,"column":106},"end":{"row":88,"column":107},"action":"remove","lines":["a"]},{"start":{"row":88,"column":105},"end":{"row":88,"column":106},"action":"remove","lines":["F"]},{"start":{"row":88,"column":104},"end":{"row":88,"column":105},"action":"remove","lines":[" "]},{"start":{"row":88,"column":103},"end":{"row":88,"column":104},"action":"remove","lines":[","]}],[{"start":{"row":69,"column":70},"end":{"row":70,"column":0},"action":"insert","lines":["",""],"id":225},{"start":{"row":70,"column":0},"end":{"row":70,"column":1},"action":"insert","lines":["t"]},{"start":{"row":70,"column":1},"end":{"row":70,"column":2},"action":"insert","lines":["o"]},{"start":{"row":70,"column":2},"end":{"row":70,"column":3},"action":"insert","lines":["t"]},{"start":{"row":70,"column":3},"end":{"row":70,"column":4},"action":"insert","lines":["a"]},{"start":{"row":70,"column":4},"end":{"row":70,"column":5},"action":"insert","lines":["l"]},{"start":{"row":70,"column":5},"end":{"row":70,"column":6},"action":"insert","lines":["_"]}],[{"start":{"row":70,"column":0},"end":{"row":70,"column":6},"action":"remove","lines":["total_"],"id":226},{"start":{"row":70,"column":0},"end":{"row":70,"column":16},"action":"insert","lines":["total_order_cost"]}],[{"start":{"row":70,"column":16},"end":{"row":70,"column":17},"action":"insert","lines":[" "],"id":227},{"start":{"row":70,"column":17},"end":{"row":70,"column":18},"action":"insert","lines":["="]}],[{"start":{"row":70,"column":18},"end":{"row":70,"column":19},"action":"insert","lines":[" "],"id":228}],[{"start":{"row":70,"column":19},"end":{"row":70,"column":40},"action":"insert","lines":["original_position_qty"],"id":229}],[{"start":{"row":70,"column":40},"end":{"row":70,"column":41},"action":"insert","lines":["*"],"id":230}],[{"start":{"row":70,"column":41},"end":{"row":70,"column":60},"action":"insert","lines":["average_entry_price"],"id":231}],[{"start":{"row":89,"column":103},"end":{"row":89,"column":104},"action":"insert","lines":[","],"id":232}],[{"start":{"row":89,"column":104},"end":{"row":89,"column":105},"action":"insert","lines":[" "],"id":233}],[{"start":{"row":89,"column":105},"end":{"row":89,"column":121},"action":"insert","lines":["total_order_cost"],"id":234}],[{"start":{"row":41,"column":0},"end":{"row":45,"column":34},"action":"remove","lines":["all_orders = api.list_orders()","    ","for order in all_orders:","    if order.symbol == symbol:","        api.cancel_order(order.id)"],"id":235},{"start":{"row":41,"column":0},"end":{"row":41,"column":37},"action":"insert","lines":["cancel_all_symbol_orders(api, symbol)"]}],[{"start":{"row":46,"column":29},"end":{"row":46,"column":42},"action":"remove","lines":["BUYING SCRIPT"],"id":236},{"start":{"row":46,"column":29},"end":{"row":46,"column":30},"action":"insert","lines":["S"]},{"start":{"row":46,"column":30},"end":{"row":46,"column":31},"action":"insert","lines":["t"]},{"start":{"row":46,"column":31},"end":{"row":46,"column":32},"action":"insert","lines":["o"]},{"start":{"row":46,"column":32},"end":{"row":46,"column":33},"action":"insert","lines":["p"]}],[{"start":{"row":46,"column":33},"end":{"row":46,"column":34},"action":"insert","lines":[" "],"id":237},{"start":{"row":46,"column":34},"end":{"row":46,"column":35},"action":"insert","lines":["L"]},{"start":{"row":46,"column":35},"end":{"row":46,"column":36},"action":"insert","lines":["o"]},{"start":{"row":46,"column":36},"end":{"row":46,"column":37},"action":"insert","lines":["s"]},{"start":{"row":46,"column":37},"end":{"row":46,"column":38},"action":"insert","lines":["s"]}],[{"start":{"row":28,"column":0},"end":{"row":29,"column":0},"action":"insert","lines":["",""],"id":238}],[{"start":{"row":28,"column":0},"end":{"row":29,"column":4},"action":"remove","lines":["","    "],"id":239}],[{"start":{"row":28,"column":0},"end":{"row":29,"column":0},"action":"insert","lines":["",""],"id":240}],[{"start":{"row":42,"column":37},"end":{"row":43,"column":0},"action":"insert","lines":["",""],"id":241},{"start":{"row":43,"column":0},"end":{"row":44,"column":0},"action":"insert","lines":["",""]}],[{"start":{"row":43,"column":0},"end":{"row":44,"column":0},"action":"remove","lines":["",""],"id":242}],[{"start":{"row":40,"column":28},"end":{"row":41,"column":0},"action":"insert","lines":["",""],"id":243},{"start":{"row":41,"column":0},"end":{"row":42,"column":0},"action":"insert","lines":["",""]}],[{"start":{"row":42,"column":0},"end":{"row":42,"column":1},"action":"insert","lines":["d"],"id":244},{"start":{"row":42,"column":1},"end":{"row":42,"column":2},"action":"insert","lines":["e"]},{"start":{"row":42,"column":2},"end":{"row":42,"column":3},"action":"insert","lines":["f"]}],[{"start":{"row":42,"column":3},"end":{"row":42,"column":4},"action":"insert","lines":[" "],"id":245},{"start":{"row":42,"column":4},"end":{"row":42,"column":5},"action":"insert","lines":["c"]},{"start":{"row":42,"column":5},"end":{"row":42,"column":6},"action":"insert","lines":["h"]},{"start":{"row":42,"column":6},"end":{"row":42,"column":7},"action":"insert","lines":["a"]},{"start":{"row":42,"column":7},"end":{"row":42,"column":8},"action":"insert","lines":["n"]},{"start":{"row":42,"column":8},"end":{"row":42,"column":9},"action":"insert","lines":["g"]},{"start":{"row":42,"column":9},"end":{"row":42,"column":10},"action":"insert","lines":["e"]}],[{"start":{"row":42,"column":10},"end":{"row":42,"column":11},"action":"insert","lines":["_"],"id":246},{"start":{"row":42,"column":11},"end":{"row":42,"column":12},"action":"insert","lines":["s"]},{"start":{"row":42,"column":12},"end":{"row":42,"column":13},"action":"insert","lines":["t"]},{"start":{"row":42,"column":13},"end":{"row":42,"column":14},"action":"insert","lines":["o"]},{"start":{"row":42,"column":14},"end":{"row":42,"column":15},"action":"insert","lines":["p"]},{"start":{"row":42,"column":15},"end":{"row":42,"column":16},"action":"insert","lines":["_"]},{"start":{"row":42,"column":16},"end":{"row":42,"column":17},"action":"insert","lines":["l"]},{"start":{"row":42,"column":17},"end":{"row":42,"column":18},"action":"insert","lines":["o"]}],[{"start":{"row":42,"column":18},"end":{"row":42,"column":19},"action":"insert","lines":["s"],"id":247},{"start":{"row":42,"column":19},"end":{"row":42,"column":20},"action":"insert","lines":["s"]}],[{"start":{"row":42,"column":20},"end":{"row":42,"column":22},"action":"insert","lines":["()"],"id":248}],[{"start":{"row":42,"column":22},"end":{"row":42,"column":23},"action":"insert","lines":[":"],"id":249}],[{"start":{"row":44,"column":0},"end":{"row":44,"column":4},"action":"insert","lines":["    "],"id":250},{"start":{"row":45,"column":0},"end":{"row":45,"column":4},"action":"insert","lines":["    "]},{"start":{"row":46,"column":0},"end":{"row":46,"column":4},"action":"insert","lines":["    "]},{"start":{"row":47,"column":0},"end":{"row":47,"column":4},"action":"insert","lines":["    "]},{"start":{"row":48,"column":0},"end":{"row":48,"column":4},"action":"insert","lines":["    "]},{"start":{"row":49,"column":0},"end":{"row":49,"column":4},"action":"insert","lines":["    "]},{"start":{"row":50,"column":0},"end":{"row":50,"column":4},"action":"insert","lines":["    "]},{"start":{"row":51,"column":0},"end":{"row":51,"column":4},"action":"insert","lines":["    "]},{"start":{"row":52,"column":0},"end":{"row":52,"column":4},"action":"insert","lines":["    "]},{"start":{"row":53,"column":0},"end":{"row":53,"column":4},"action":"insert","lines":["    "]},{"start":{"row":54,"column":0},"end":{"row":54,"column":4},"action":"insert","lines":["    "]},{"start":{"row":55,"column":0},"end":{"row":55,"column":4},"action":"insert","lines":["    "]},{"start":{"row":56,"column":0},"end":{"row":56,"column":4},"action":"insert","lines":["    "]},{"start":{"row":57,"column":0},"end":{"row":57,"column":4},"action":"insert","lines":["    "]},{"start":{"row":58,"column":0},"end":{"row":58,"column":4},"action":"insert","lines":["    "]},{"start":{"row":59,"column":0},"end":{"row":59,"column":4},"action":"insert","lines":["    "]},{"start":{"row":60,"column":0},"end":{"row":60,"column":4},"action":"insert","lines":["    "]},{"start":{"row":61,"column":0},"end":{"row":61,"column":4},"action":"insert","lines":["    "]},{"start":{"row":62,"column":0},"end":{"row":62,"column":4},"action":"insert","lines":["    "]},{"start":{"row":63,"column":0},"end":{"row":63,"column":4},"action":"insert","lines":["    "]},{"start":{"row":64,"column":0},"end":{"row":64,"column":4},"action":"insert","lines":["    "]},{"start":{"row":65,"column":0},"end":{"row":65,"column":4},"action":"insert","lines":["    "]},{"start":{"row":66,"column":0},"end":{"row":66,"column":4},"action":"insert","lines":["    "]},{"start":{"row":67,"column":0},"end":{"row":67,"column":4},"action":"insert","lines":["    "]},{"start":{"row":68,"column":0},"end":{"row":68,"column":4},"action":"insert","lines":["    "]},{"start":{"row":69,"column":0},"end":{"row":69,"column":4},"action":"insert","lines":["    "]},{"start":{"row":70,"column":0},"end":{"row":70,"column":4},"action":"insert","lines":["    "]},{"start":{"row":71,"column":0},"end":{"row":71,"column":4},"action":"insert","lines":["    "]},{"start":{"row":72,"column":0},"end":{"row":72,"column":4},"action":"insert","lines":["    "]},{"start":{"row":73,"column":0},"end":{"row":73,"column":4},"action":"insert","lines":["    "]},{"start":{"row":74,"column":0},"end":{"row":74,"column":4},"action":"insert","lines":["    "]},{"start":{"row":75,"column":0},"end":{"row":75,"column":4},"action":"insert","lines":["    "]},{"start":{"row":76,"column":0},"end":{"row":76,"column":4},"action":"insert","lines":["    "]},{"start":{"row":77,"column":0},"end":{"row":77,"column":4},"action":"insert","lines":["    "]},{"start":{"row":78,"column":0},"end":{"row":78,"column":4},"action":"insert","lines":["    "]},{"start":{"row":79,"column":0},"end":{"row":79,"column":4},"action":"insert","lines":["    "]},{"start":{"row":80,"column":0},"end":{"row":80,"column":4},"action":"insert","lines":["    "]},{"start":{"row":81,"column":0},"end":{"row":81,"column":4},"action":"insert","lines":["    "]},{"start":{"row":82,"column":0},"end":{"row":82,"column":4},"action":"insert","lines":["    "]},{"start":{"row":83,"column":0},"end":{"row":83,"column":4},"action":"insert","lines":["    "]},{"start":{"row":84,"column":0},"end":{"row":84,"column":4},"action":"insert","lines":["    "]},{"start":{"row":85,"column":0},"end":{"row":85,"column":4},"action":"insert","lines":["    "]},{"start":{"row":86,"column":0},"end":{"row":86,"column":4},"action":"insert","lines":["    "]},{"start":{"row":87,"column":0},"end":{"row":87,"column":4},"action":"insert","lines":["    "]},{"start":{"row":88,"column":0},"end":{"row":88,"column":4},"action":"insert","lines":["    "]},{"start":{"row":89,"column":0},"end":{"row":89,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":42,"column":21},"end":{"row":42,"column":22},"action":"insert","lines":["a"],"id":251},{"start":{"row":42,"column":22},"end":{"row":42,"column":23},"action":"insert","lines":["p"]},{"start":{"row":42,"column":23},"end":{"row":42,"column":24},"action":"insert","lines":["i"]},{"start":{"row":42,"column":24},"end":{"row":42,"column":25},"action":"insert","lines":[","]}],[{"start":{"row":42,"column":25},"end":{"row":42,"column":26},"action":"insert","lines":[" "],"id":252},{"start":{"row":42,"column":26},"end":{"row":42,"column":27},"action":"insert","lines":["s"]},{"start":{"row":42,"column":27},"end":{"row":42,"column":28},"action":"insert","lines":["y"]},{"start":{"row":42,"column":28},"end":{"row":42,"column":29},"action":"insert","lines":["m"]},{"start":{"row":42,"column":29},"end":{"row":42,"column":30},"action":"insert","lines":["b"]},{"start":{"row":42,"column":30},"end":{"row":42,"column":31},"action":"insert","lines":["o"]},{"start":{"row":42,"column":31},"end":{"row":42,"column":32},"action":"insert","lines":["l"]}],[{"start":{"row":31,"column":0},"end":{"row":31,"column":22},"action":"remove","lines":["extended_hours = False"],"id":253}],[{"start":{"row":30,"column":0},"end":{"row":31,"column":0},"action":"remove","lines":["",""],"id":254},{"start":{"row":29,"column":0},"end":{"row":30,"column":0},"action":"remove","lines":["",""]},{"start":{"row":28,"column":0},"end":{"row":29,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":39,"column":34},"end":{"row":40,"column":0},"action":"insert","lines":["",""],"id":255},{"start":{"row":40,"column":0},"end":{"row":40,"column":4},"action":"insert","lines":["    "]},{"start":{"row":40,"column":4},"end":{"row":41,"column":0},"action":"insert","lines":["",""]},{"start":{"row":41,"column":0},"end":{"row":41,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":41,"column":4},"end":{"row":41,"column":26},"action":"insert","lines":["extended_hours = False"],"id":256}],[{"start":{"row":30,"column":0},"end":{"row":37,"column":28},"action":"remove","lines":["api = tradeapi.REST(","        API_KEY,","        SECRET_KEY,","        BASE_URL","    )","    ","    ","symbol = sys.argv[2].upper()"],"id":257}],[{"start":{"row":29,"column":4},"end":{"row":30,"column":0},"action":"remove","lines":["",""],"id":258},{"start":{"row":29,"column":0},"end":{"row":29,"column":4},"action":"remove","lines":["    "]},{"start":{"row":28,"column":0},"end":{"row":29,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":82,"column":0},"end":{"row":83,"column":0},"action":"insert","lines":["",""],"id":259},{"start":{"row":83,"column":0},"end":{"row":83,"column":1},"action":"insert","lines":["i"]},{"start":{"row":83,"column":1},"end":{"row":83,"column":2},"action":"insert","lines":["f"]}],[{"start":{"row":83,"column":2},"end":{"row":83,"column":3},"action":"insert","lines":[" "],"id":260},{"start":{"row":83,"column":3},"end":{"row":83,"column":4},"action":"insert","lines":["m"]},{"start":{"row":83,"column":4},"end":{"row":83,"column":5},"action":"insert","lines":["a"]},{"start":{"row":83,"column":5},"end":{"row":83,"column":6},"action":"insert","lines":["i"]},{"start":{"row":83,"column":6},"end":{"row":83,"column":7},"action":"insert","lines":["n"]},{"start":{"row":83,"column":7},"end":{"row":83,"column":8},"action":"insert","lines":[":"]}],[{"start":{"row":83,"column":8},"end":{"row":83,"column":12},"action":"remove","lines":["    "],"id":261},{"start":{"row":83,"column":8},"end":{"row":84,"column":0},"action":"insert","lines":["",""]},{"start":{"row":84,"column":0},"end":{"row":84,"column":4},"action":"insert","lines":["    "]},{"start":{"row":84,"column":4},"end":{"row":85,"column":0},"action":"insert","lines":["",""]},{"start":{"row":85,"column":0},"end":{"row":85,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":85,"column":4},"end":{"row":92,"column":28},"action":"insert","lines":["api = tradeapi.REST(","        API_KEY,","        SECRET_KEY,","        BASE_URL","    )","    ","    ","symbol = sys.argv[2].upper()"],"id":262}],[{"start":{"row":92,"column":0},"end":{"row":92,"column":4},"action":"insert","lines":["    "],"id":263}],[{"start":{"row":83,"column":0},"end":{"row":83,"column":8},"action":"remove","lines":["if main:"],"id":264},{"start":{"row":83,"column":0},"end":{"row":83,"column":26},"action":"insert","lines":["if __name__ == '__main__':"]}],[{"start":{"row":92,"column":32},"end":{"row":93,"column":0},"action":"insert","lines":["",""],"id":265},{"start":{"row":93,"column":0},"end":{"row":93,"column":4},"action":"insert","lines":["    "]},{"start":{"row":93,"column":4},"end":{"row":94,"column":0},"action":"insert","lines":["",""]},{"start":{"row":94,"column":0},"end":{"row":94,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":94,"column":4},"end":{"row":94,"column":33},"action":"insert","lines":["change_stop_loss(api, symbol)"],"id":266}],[{"start":{"row":52,"column":4},"end":{"row":57,"column":14},"action":"remove","lines":["if len(sys.argv) > 3 and sys.argv[3] != 0:","        #This will be a limit buy","        stop_limit_price = float(sys.argv[3])","    else:","        print(\"Error, need stop_limit price exiting...\")","        exit()"],"id":267}],[{"start":{"row":52,"column":0},"end":{"row":52,"column":4},"action":"remove","lines":["    "],"id":268},{"start":{"row":51,"column":4},"end":{"row":52,"column":0},"action":"remove","lines":["",""]},{"start":{"row":51,"column":0},"end":{"row":51,"column":4},"action":"remove","lines":["    "]},{"start":{"row":50,"column":61},"end":{"row":51,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":85,"column":32},"end":{"row":86,"column":0},"action":"insert","lines":["",""],"id":269},{"start":{"row":86,"column":0},"end":{"row":86,"column":4},"action":"insert","lines":["    "]},{"start":{"row":86,"column":4},"end":{"row":87,"column":0},"action":"insert","lines":["",""]},{"start":{"row":87,"column":0},"end":{"row":87,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":87,"column":4},"end":{"row":92,"column":14},"action":"insert","lines":["if len(sys.argv) > 3 and sys.argv[3] != 0:","        #This will be a limit buy","        stop_limit_price = float(sys.argv[3])","    else:","        print(\"Error, need stop_limit price exiting...\")","        exit()"],"id":270}],[{"start":{"row":94,"column":32},"end":{"row":94,"column":33},"action":"insert","lines":[","],"id":271}],[{"start":{"row":94,"column":33},"end":{"row":94,"column":34},"action":"insert","lines":[" "],"id":272}],[{"start":{"row":94,"column":34},"end":{"row":94,"column":50},"action":"insert","lines":["stop_limit_price"],"id":273}],[{"start":{"row":30,"column":32},"end":{"row":30,"column":33},"action":"insert","lines":[","],"id":274}],[{"start":{"row":30,"column":33},"end":{"row":30,"column":34},"action":"insert","lines":[" "],"id":275}],[{"start":{"row":30,"column":34},"end":{"row":30,"column":50},"action":"insert","lines":["stop_limit_price"],"id":276}],[{"start":{"row":94,"column":51},"end":{"row":95,"column":0},"action":"insert","lines":["",""],"id":277},{"start":{"row":95,"column":0},"end":{"row":95,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":94,"column":51},"end":{"row":95,"column":0},"action":"insert","lines":["",""],"id":278},{"start":{"row":95,"column":0},"end":{"row":95,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":95,"column":4},"end":{"row":96,"column":0},"action":"insert","lines":["",""],"id":279},{"start":{"row":96,"column":0},"end":{"row":96,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":34,"column":4},"end":{"row":34,"column":5},"action":"insert","lines":["u"],"id":280},{"start":{"row":34,"column":5},"end":{"row":34,"column":6},"action":"insert","lines":["t"]},{"start":{"row":34,"column":6},"end":{"row":34,"column":7},"action":"insert","lines":["."]}]]},"ace":{"folds":[],"scrolltop":397,"scrollleft":0,"selection":{"start":{"row":38,"column":4},"end":{"row":38,"column":4},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":109,"mode":"ace/mode/python"}},"timestamp":1626454934315,"hash":"4ed440a725faeb505f44566e2d2a5aecac473330"}