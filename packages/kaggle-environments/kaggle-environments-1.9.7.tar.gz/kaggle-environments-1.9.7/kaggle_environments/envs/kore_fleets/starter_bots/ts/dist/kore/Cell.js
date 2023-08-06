"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Cell = void 0;
var Direction_1 = require("./Direction");
var Cell = /** @class */ (function () {
    function Cell(position, kore, shipyardId, fleetId, board) {
        this.position = position;
        this.kore = kore;
        this.shipyardId = shipyardId;
        this.fleetId = fleetId;
        this.board = board;
    }
    Cell.prototype.cloneToBoard = function (board) {
        return new Cell(this.position, this.kore, this.shipyardId, this.fleetId, board);
    };
    Object.defineProperty(Cell.prototype, "fleet", {
        get: function () {
            if (this.board.fleets.has(this.fleetId)) {
                return this.board.fleets.get(this.fleetId);
            }
            return undefined;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Cell.prototype, "shipyard", {
        get: function () {
            if (this.board.shipyards.has(this.shipyardId)) {
                return this.board.shipyards.get(this.shipyardId);
            }
            return undefined;
        },
        enumerable: false,
        configurable: true
    });
    Cell.prototype.neighbor = function (offset) {
        var next = this.position.translate(offset, this.board.size);
        return this.board.getCellAtPosition(next);
    };
    Cell.prototype.north = function () {
        return this.neighbor(Direction_1.Direction.NORTH);
    };
    Cell.prototype.south = function () {
        return this.neighbor((Direction_1.Direction.SOUTH));
    };
    Cell.prototype.east = function () {
        return this.neighbor(Direction_1.Direction.EAST);
    };
    Cell.prototype.west = function () {
        return this.neighbor(Direction_1.Direction.WEST);
    };
    return Cell;
}());
exports.Cell = Cell;
//# sourceMappingURL=Cell.js.map