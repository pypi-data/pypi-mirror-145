"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.Direction = void 0;
var Point_1 = require("./Point");
var Direction = /** @class */ (function (_super) {
    __extends(Direction, _super);
    function Direction(x, y) {
        return _super.call(this, x, y) || this;
    }
    Direction.prototype.equals = function (other) {
        return this.x == other.x && this.y == other.y;
    };
    Direction.prototype.rotateLeft = function () {
        if (this.equals(Direction.NORTH)) {
            return Direction.WEST;
        }
        if (this.equals(Direction.WEST)) {
            return Direction.SOUTH;
        }
        if (this.equals(Direction.SOUTH)) {
            return Direction.EAST;
        }
        if (this.equals(Direction.EAST)) {
            return Direction.NORTH;
        }
        throw new Error("invalid direction");
    };
    Direction.prototype.rotateRight = function () {
        if (this.equals(Direction.NORTH)) {
            return Direction.EAST;
        }
        if (this.equals(Direction.EAST)) {
            return Direction.SOUTH;
        }
        if (this.equals(Direction.SOUTH)) {
            return Direction.WEST;
        }
        if (this.equals(Direction.WEST)) {
            return Direction.NORTH;
        }
        throw new Error("invalid direction");
    };
    Direction.prototype.opposite = function () {
        if (this.equals(Direction.NORTH)) {
            return Direction.SOUTH;
        }
        if (this.equals(Direction.EAST)) {
            return Direction.WEST;
        }
        if (this.equals(Direction.SOUTH)) {
            return Direction.NORTH;
        }
        if (this.equals(Direction.WEST)) {
            return Direction.EAST;
        }
        throw new Error("invalid direction");
    };
    Direction.prototype.toChar = function () {
        if (this.equals(Direction.NORTH)) {
            return "N";
        }
        if (this.equals(Direction.EAST)) {
            return "E";
        }
        if (this.equals(Direction.SOUTH)) {
            return "S";
        }
        if (this.equals(Direction.WEST)) {
            return "W";
        }
        throw new Error("invalid direction");
    };
    Direction.prototype.toString = function () {
        if (this.equals(Direction.NORTH)) {
            return "NORTH";
        }
        if (this.equals(Direction.EAST)) {
            return "EAST";
        }
        if (this.equals(Direction.SOUTH)) {
            return "SOUTH";
        }
        if (this.equals(Direction.WEST)) {
            return "WEST";
        }
        throw new Error("invalid direction");
    };
    Direction.prototype.toIndex = function () {
        if (this.equals(Direction.NORTH)) {
            return 0;
        }
        if (this.equals(Direction.EAST)) {
            return 1;
        }
        if (this.equals(Direction.SOUTH)) {
            return 2;
        }
        if (this.equals(Direction.WEST)) {
            return 3;
        }
        throw new Error("invalid direction");
    };
    Direction.fromString = function (dirStr) {
        switch (dirStr) {
            case "NORTH":
                return Direction.NORTH;
            case "EAST":
                return Direction.EAST;
            case "SOUTH":
                return Direction.SOUTH;
            case "WEST":
                return Direction.WEST;
        }
        throw new Error("invalid direction");
    };
    Direction.fromChar = function (dirChar) {
        switch (dirChar) {
            case 'N':
                return Direction.NORTH;
            case 'E':
                return Direction.EAST;
            case 'S':
                return Direction.SOUTH;
            case 'W':
                return Direction.WEST;
        }
        throw new Error("invalid direction");
    };
    Direction.fromIndex = function (index) {
        switch (index) {
            case 0:
                return Direction.NORTH;
            case 1:
                return Direction.EAST;
            case 2:
                return Direction.SOUTH;
            case 3:
                return Direction.WEST;
        }
        throw new Error("invalid direction");
    };
    Direction.listDirections = function () {
        return [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST
        ];
    };
    Direction.NORTH = new Direction(0, 1);
    Direction.EAST = new Direction(1, 0);
    Direction.SOUTH = new Direction(0, -1);
    Direction.WEST = new Direction(-1, 0);
    return Direction;
}(Point_1.Point));
exports.Direction = Direction;
//# sourceMappingURL=Direction.js.map