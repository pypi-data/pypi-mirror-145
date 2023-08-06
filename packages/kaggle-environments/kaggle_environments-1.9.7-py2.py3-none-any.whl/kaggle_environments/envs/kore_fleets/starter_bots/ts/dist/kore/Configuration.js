"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Configuration = void 0;
var Configuration = /** @class */ (function () {
    function Configuration(rawConfiguration) {
        var config = JSON.parse(rawConfiguration);
        this.agentTimeout = config.agentTimeout;
        this.startingKore = config.startingKore;
        this.size = config.size;
        this.spawnCost = config.spawnCost;
        this.convertCost = config.convertCost;
        this.regenRate = config.regenRate;
        this.maxRegenCellKore = config.maxRegenCellKore;
        this.randomSeed = config.randomSeed;
    }
    return Configuration;
}());
exports.Configuration = Configuration;
//# sourceMappingURL=Configuration.js.map