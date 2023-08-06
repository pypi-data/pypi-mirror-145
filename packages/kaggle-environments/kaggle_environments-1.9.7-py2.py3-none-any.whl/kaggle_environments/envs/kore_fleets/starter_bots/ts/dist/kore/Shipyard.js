"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Shipyard = void 0;
var SPAWN_VALUES = [];
var upgradeTimes = [];
for (var i = 1; i < 10; i++) {
    upgradeTimes[i - 1] = Math.pow(i, 2) + 1;
}
var current = 0;
for (var i = 1; i < 10; i++) {
    current += upgradeTimes[i - 1];
    SPAWN_VALUES[i - 1] = current;
}
var Shipyard = /** @class */ (function () {
    function Shipyard(shipyardId, shipCount, position, playerId, turnsControlled, board, nextAction) {
        this.id = shipyardId;
        this.shipCount = shipCount;
        this.position = position;
        this.playerId = playerId;
        this.turnsControlled = turnsControlled;
        this.board = board;
        this.nextAction = nextAction;
    }
    Shipyard.prototype.cloneToBoard = function (board) {
        return new Shipyard(this.id, this.shipCount, this.position, this.playerId, this.turnsControlled, board, this.nextAction);
    };
    Shipyard.prototype.setNextAction = function (action) {
        this.nextAction = action;
    };
    Object.defineProperty(Shipyard.prototype, "maxSpawn", {
        get: function () {
            for (var i = 0; i < SPAWN_VALUES.length; i++) {
                if (this.turnsControlled < SPAWN_VALUES[i]) {
                    return i + 1;
                }
            }
            return SPAWN_VALUES.length + 1;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Shipyard.prototype, "cell", {
        /**
         *  Returns the cell this shipyard is on.
         */
        get: function () {
            return this.board.getCellAtPosition(this.position);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Shipyard.prototype, "player", {
        get: function () {
            return this.board.players[this.playerId];
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Converts a shipyard back to the normalized observation subset that constructed it.
     */
    Shipyard.prototype.observation = function () {
        return [this.position.toIndex(this.board.configuration.size), this.shipCount, this.turnsControlled];
    };
    return Shipyard;
}());
exports.Shipyard = Shipyard;
//# sourceMappingURL=Shipyard.js.map