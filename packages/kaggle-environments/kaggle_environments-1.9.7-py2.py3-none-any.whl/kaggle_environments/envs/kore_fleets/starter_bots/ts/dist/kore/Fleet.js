"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Fleet = void 0;
var Fleet = /** @class */ (function () {
    function Fleet(fleetId, shipCount, direction, position, kore, flightPlan, playerId, board) {
        this.id = fleetId;
        this.shipCount = shipCount;
        this.direction = direction;
        this.position = position;
        this.flightPlan = flightPlan;
        this.kore = kore;
        this.playerId = playerId;
        this.board = board;
    }
    Fleet.prototype.cloneToBoard = function (board) {
        return new Fleet(this.id, this.shipCount, this.direction, this.position, this.kore, this.flightPlan, this.playerId, board);
    };
    Object.defineProperty(Fleet.prototype, "cell", {
        get: function () {
            return this.board.getCellAtPosition(this.position);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Fleet.prototype, "player", {
        get: function () {
            return this.board.players[this.playerId];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Fleet.prototype, "collectionRate", {
        get: function () {
            return Math.min(Math.log(this.shipCount) / 10, .99);
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Returns the length of the longest possible flight plan this fleet can be assigned
     * @return
     */
    Fleet.maxFlightPlanLenForShipCount = function (shipCount) {
        return (Math.floor(2 * Math.log(shipCount)) + 1);
    };
    /**
     * Converts a fleet back to the normalized observation subset that constructed it.
     */
    Fleet.prototype.observation = function () {
        return [
            this.position.toIndex(this.board.configuration.size).toString(),
            this.kore.toString(),
            this.shipCount.toString(),
            this.direction.toIndex().toString(),
            this.flightPlan
        ];
    };
    Fleet.prototype.lessThanOtherAlliedFleet = function (other) {
        if (this.shipCount != other.shipCount) {
            return this.shipCount < other.shipCount;
        }
        if (this.kore != other.kore) {
            return this.kore < other.kore;
        }
        return this.direction.toIndex() > other.direction.toIndex();
    };
    return Fleet;
}());
exports.Fleet = Fleet;
//# sourceMappingURL=Fleet.js.map