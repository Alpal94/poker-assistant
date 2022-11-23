from flask import Flask
import traceback
import preflop
import hud

app = Flask(__name__)


@app.route('/')
def hello():
    try:
        hand = [{
                "rank": "7",
                "suit": "c"
            },{
                "rank": "3",
                "suit": "d"

            }
        ]
        if preflop.handRangeDecision(hand, 'UTG', 'RFI'):
            return 'Recommended to play hand'
        return 'Fold'
    except Exception as e:
        print(traceback.format_exc())
        return "Error: " + str(e)

if __name__ == '__main__':
    app.run()

app.route(rule, options)
app.run(host, port, debug, options)
