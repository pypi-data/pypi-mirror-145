"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Direction_1 = require("./kore/Direction");
var ShipyardAction_1 = require("./kore/ShipyardAction");
var KoreIO_1 = require("./kore/KoreIO");
var io = new KoreIO_1.KoreIO();
// agent.run takes care of running your code per tick
io.run(function (board) {
    var me = board.currentPlayer;
    var turn = board.step;
    var spawnCost = board.configuration.spawnCost;
    var koreLeft = me.kore;
    for (var _i = 0, _a = me.shipyards; _i < _a.length; _i++) {
        var shipyard = _a[_i];
        if (shipyard.shipCount > 10) {
            var dir = Direction_1.Direction.fromIndex(turn % 4);
            var action = ShipyardAction_1.ShipyardAction.launchFleetWithFlightPlan(2, dir.toChar());
            shipyard.setNextAction(action);
        }
        else if (koreLeft > spawnCost * shipyard.maxSpawn) {
            var action = ShipyardAction_1.ShipyardAction.spawnShips(shipyard.maxSpawn);
            shipyard.setNextAction(action);
            koreLeft -= spawnCost * shipyard.maxSpawn;
        }
        else if (koreLeft > spawnCost) {
            var action = ShipyardAction_1.ShipyardAction.spawnShips(1);
            shipyard.setNextAction(action);
            koreLeft -= spawnCost;
        }
    }
    // nextActions will be pulled off of your shipyards
    return board;
});
//# sourceMappingURL=Bot.js.map