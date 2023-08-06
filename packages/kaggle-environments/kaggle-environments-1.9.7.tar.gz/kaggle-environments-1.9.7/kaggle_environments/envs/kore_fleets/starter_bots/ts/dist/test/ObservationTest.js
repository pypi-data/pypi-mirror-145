"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var mocha_1 = require("mocha");
var chai_1 = require("chai");
var fs = __importStar(require("fs"));
var Observation_1 = require("../kore/Observation");
(0, mocha_1.describe)('Observation', function () {
    it('valid observation works', function () {
        var rawObs = fs.readFileSync('./test/observation.json', 'utf8');
        var ob = new Observation_1.Observation(rawObs);
        (0, chai_1.expect)(ob.player).to.equal(0);
        (0, chai_1.expect)(ob.step).to.equal(16);
        (0, chai_1.expect)(ob.playerFleets.length).to.equal(4);
        (0, chai_1.expect)(ob.playerFleets[0].size).to.equal(0);
        (0, chai_1.expect)(ob.playerShipyards.length).to.equal(4);
        (0, chai_1.expect)(ob.playerShipyards[0].size).to.equal(1);
    });
    it('full observation works', function () {
        var rawObs = fs.readFileSync('./test/fullob.json', 'utf8');
        var ob = new Observation_1.Observation(rawObs);
        (0, chai_1.expect)(ob.player).to.equal(0);
        (0, chai_1.expect)(ob.step).to.equal(200);
        (0, chai_1.expect)(ob.playerHlt.length).to.equal(2);
        (0, chai_1.expect)(ob.playerFleets.length).to.equal(2);
        (0, chai_1.expect)(ob.playerFleets[0].size).to.equal(1);
        (0, chai_1.expect)(ob.playerShipyards.length).to.equal(2);
        (0, chai_1.expect)(ob.playerShipyards[0].size).to.equal(6);
    });
});
//# sourceMappingURL=ObservationTest.js.map