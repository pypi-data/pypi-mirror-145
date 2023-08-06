"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Observation = void 0;
var Observation = /** @class */ (function () {
    function Observation(rawObservation) {
        var json = JSON.parse(rawObservation);
        this.kore = json["kore"];
        this.player = json["player"];
        this.step = json["step"];
        this.remainingOverageTime = rawObservation["remainingOverageTime"];
        var playerParts = json["players"];
        this.playerHlt = [];
        this.playerShipyards = [];
        this.playerFleets = [];
        var _loop_1 = function () {
            var playerPart = playerParts[i];
            this_1.playerHlt.push(parseInt(playerPart[0]));
            var shipyards = new Map();
            Object.entries(playerPart[1]).forEach(function (entry) {
                var shipyardId = entry[0];
                var shipyardInts = entry[1];
                shipyards.set(shipyardId, shipyardInts);
            });
            this_1.playerShipyards.push(shipyards);
            var fleets = new Map();
            Object.entries(playerPart[2]).forEach(function (entry) {
                var fleetId = entry[0];
                var fleetStrs = entry[1];
                fleets.set(fleetId, fleetStrs);
            });
            this_1.playerFleets.push(fleets);
        };
        var this_1 = this;
        for (var i = 0; i < playerParts.length; i++) {
            _loop_1();
        }
    }
    return Observation;
}());
exports.Observation = Observation;
//# sourceMappingURL=Observation.js.map