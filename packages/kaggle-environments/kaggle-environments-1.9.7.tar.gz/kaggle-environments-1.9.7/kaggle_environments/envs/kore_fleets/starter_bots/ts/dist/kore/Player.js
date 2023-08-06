"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Player = void 0;
var Player = /** @class */ (function () {
    function Player(playerId, kore, shipyardIds, fleetIds, board) {
        this.id = playerId;
        this.kore = kore;
        this.shipyardIds = shipyardIds;
        this.fleetIds = fleetIds;
        this.board = board;
    }
    Player.prototype.cloneToBoard = function (board) {
        return new Player(this.id, this.kore, this.shipyardIds.slice(), this.fleetIds.slice(), board);
    };
    Object.defineProperty(Player.prototype, "shipyards", {
        /**
         * Returns all shipyards owned by this player.
         * @return
         */
        get: function () {
            var _this = this;
            return Array.from(this.board.shipyards.values())
                .filter(function (shipyard) { return _this.shipyardIds.some(function (sId) { return sId == shipyard.id; }); });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Player.prototype, "fleets", {
        /**
         * Returns all fleets owned by this player.
         */
        get: function () {
            var _this = this;
            return Array.from(this.board.fleets.values())
                .filter(function (fleet) { return _this.fleetIds.some(function (fId) { return fId == fleet.id; }); });
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Returns whether this player is the current player (generally if this returns True, this player is you.
     */
    Player.prototype.isCurrentPlayer = function () {
        return this.id == this.board.currentPlayerId;
    };
    Object.defineProperty(Player.prototype, "nextActions", {
        /**
         * Returns all queued fleet and shipyard actions for this player formatted for the kore interpreter to receive as an agent response.
         */
        get: function () {
            var result = new Map();
            this.shipyards.filter(function (shipyard) { return shipyard.nextAction; }).forEach(function (shipyard) { return result.set(shipyard.id, shipyard.nextAction); });
            return result;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Converts a player back to the normalized observation subset that constructed it.
     */
    Player.prototype.observation = function () {
        var shipyards = new Map();
        this.shipyards.forEach(function (shipyard) { return shipyards.set(shipyard.id, shipyard.observation()); });
        var fleets = new Map();
        this.fleets.forEach(function (fleet) { return fleets.set(fleet.id, fleet.observation()); });
        return [this.kore, shipyards, fleets];
    };
    return Player;
}());
exports.Player = Player;
//# sourceMappingURL=Player.js.map