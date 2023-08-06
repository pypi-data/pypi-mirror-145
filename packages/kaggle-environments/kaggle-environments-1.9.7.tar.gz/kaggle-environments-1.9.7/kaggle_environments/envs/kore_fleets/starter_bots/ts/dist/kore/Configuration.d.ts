export declare class Configuration {
    readonly agentTimeout: number;
    readonly startingKore: number;
    readonly size: number;
    readonly spawnCost: number;
    readonly convertCost: number;
    readonly regenRate: number;
    readonly maxRegenCellKore: number;
    readonly randomSeed: number;
    constructor(rawConfiguration: string);
}
