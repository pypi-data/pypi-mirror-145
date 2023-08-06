"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Point = void 0;
var Point = /** @class */ (function () {
    function Point(x, y) {
        this.x = x;
        this.y = y;
    }
    Point.prototype.translate = function (offset, size) {
        return this.add(offset).mod(size);
    };
    Point.prototype.add = function (other) {
        return new Point(this.x + other.x, this.y + other.y);
    };
    Point.prototype.mod = function (size) {
        return new Point(this.x % size, this.y % size);
    };
    /**
     * Gets the manhatten distance between two points
     */
    Point.prototype.distanceTo = function (other, size) {
        var abs_x = Math.abs(this.x - other.x);
        var dist_x = abs_x < size / 2 ? abs_x : size - abs_x;
        var abs_y = Math.abs(this.y - other.y);
        var dist_y = abs_y < size / 2 ? abs_y : size - abs_y;
        return dist_x + dist_y;
    };
    /**
     * Converts a 2d position in the form (x, y) to an index in the observation.kore list.
     * See fromIndex for the inverse.
     */
    Point.prototype.toIndex = function (size) {
        return (size - this.y - 1) * size + this.x;
    };
    Point.fromIndex = function (index, size) {
        return new Point(index % size, size - Math.floor(index / size) - 1);
    };
    Point.prototype.abs = function () {
        return new Point(Math.abs(this.x), Math.abs(this.y));
    };
    Point.prototype.equals = function (other) {
        return this.x == other.x && this.y == other.y;
    };
    Point.prototype.toString = function () {
        return "(" + this.x + "," + this.y + ")";
    };
    Point.prototype.multiply = function (factor) {
        return new Point(factor * this.x, factor * this.y);
    };
    Point.prototype.subtract = function (other) {
        return new Point(this.x - other.x, this.y - other.y);
    };
    return Point;
}());
exports.Point = Point;
//# sourceMappingURL=Point.js.map