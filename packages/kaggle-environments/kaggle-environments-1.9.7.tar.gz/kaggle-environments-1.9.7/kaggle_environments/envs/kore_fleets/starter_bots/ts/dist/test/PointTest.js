"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var mocha_1 = require("mocha");
var chai_1 = require("chai");
var Point_1 = require("../kore/Point");
(0, mocha_1.describe)('Point', function () {
    it('fontIndex toIndex isIdetity', function () {
        var idx = 254;
        var size = 31;
        var point = Point_1.Point.fromIndex(idx, size);
        var mirroredIdx = point.toIndex(size);
        (0, chai_1.expect)(mirroredIdx).to.equal(idx);
    });
});
//# sourceMappingURL=PointTest.js.map