"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var mocha_1 = require("mocha");
var chai_1 = require("chai");
var Shipyard_1 = require("../kore/Shipyard");
var Point_1 = require("../kore/Point");
(0, mocha_1.describe)('Shipyard', function () {
    var turns = [0, 1, 2, 293, 294, 295];
    var expected = [1, 1, 2, 9, 10, 10];
    var _loop_1 = function (i) {
        it("max spawn is correct at ".concat(turns[i], " turns controlled"), function () {
            var shipyard = new Shipyard_1.Shipyard("A", 0, new Point_1.Point(0, 0), 1, turns[i], null, null);
            (0, chai_1.expect)(shipyard.maxSpawn).to.equal(expected[i]);
        });
    };
    for (var i = 0; i < turns.length; i++) {
        _loop_1(i);
    }
});
//# sourceMappingURL=ShipyardTest.js.map