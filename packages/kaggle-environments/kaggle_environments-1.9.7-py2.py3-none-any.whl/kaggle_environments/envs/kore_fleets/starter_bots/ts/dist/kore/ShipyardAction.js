"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ShipyardAction = void 0;
var ShipyardAction = /** @class */ (function () {
    function ShipyardAction(type, shipCount, flightPlan) {
        // assert type.equals(SPAWN) || type.equals(LAUNCH) : "Type must be SPAWN or LAUNCH";
        // assert shipCount > 0 : "numShips must be a non-negative number";
        this.actionType = type;
        this.shipCount = shipCount;
        this.flightPlan = flightPlan;
    }
    ShipyardAction.spawnShips = function (shipCount) {
        return new ShipyardAction(ShipyardAction.SPAWN, shipCount, "");
    };
    ShipyardAction.launchFleetWithFlightPlan = function (shipCount, flightPlan) {
        return new ShipyardAction(ShipyardAction.LAUNCH, shipCount, flightPlan);
    };
    ShipyardAction.fromstring = function (raw) {
        if (raw.length == 0) {
            throw new Error("invalid raw shipyard empty string");
        }
        var shipCount = parseInt(raw.split("_")[1]);
        if (raw.startsWith(ShipyardAction.LAUNCH)) {
            return ShipyardAction.spawnShips(shipCount);
        }
        if (raw.startsWith(ShipyardAction.SPAWN)) {
            var flightPlan = raw.split("_")[2];
            return ShipyardAction.launchFleetWithFlightPlan(shipCount, flightPlan);
        }
        throw new Error("invalid Shipyard Action raw " + raw);
    };
    Object.defineProperty(ShipyardAction.prototype, "isSpawn", {
        get: function () {
            return this.actionType == ShipyardAction.SPAWN;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ShipyardAction.prototype, "isLaunch", {
        get: function () {
            return this.actionType == ShipyardAction.LAUNCH;
        },
        enumerable: false,
        configurable: true
    });
    ShipyardAction.prototype.toString = function () {
        if (this.isSpawn) {
            return "".concat(ShipyardAction.SPAWN, "_").concat(this.shipCount);
        }
        if (this.isLaunch) {
            return "".concat(ShipyardAction.LAUNCH, "_").concat(this.shipCount, "_").concat(this.flightPlan);
        }
        throw new Error("invalid Shpyard Action");
    };
    ShipyardAction.SPAWN = "SPAWN";
    ShipyardAction.LAUNCH = "LAUNCH";
    return ShipyardAction;
}());
exports.ShipyardAction = ShipyardAction;
//# sourceMappingURL=ShipyardAction.js.map